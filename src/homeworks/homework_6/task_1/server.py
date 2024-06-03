import socket
import time
from dataclasses import dataclass
from threading import Thread
from typing import Any, Optional

from loguru import logger

# RESPONSE CODES
# ROOM ERROR CODES
# 101 - ROOM ALREADY EXISTED
# 102 - ROOM NOT EXIST
# 103 - ROOM IS FULL
# ROOM SUCCEED CODES
# 202 - CONNECTED TO ROOM
# COMMAND ERROR CODES
# 301 - UNEXPECTED COMMAND


# COMMANDS CODES
# 1 - CREATE ROOM
# 2 - CONNECT TO ROOM


@dataclass
class Player:
    socket: socket.socket
    addr: Any


class Room:
    def __init__(self, name: str):
        self.name = name
        self.players: list[Any] = [None, None]
        self.current_player: int = 0

    def give_response(self, data: bytes) -> None:
        command = data.decode()
        first_index, second_index, sign, port = command.split(",")
        current_player = self.players[self.current_player]
        if not all(self.players):
            logger.error("Not enough players")
            return
        if int(port) == int(current_player.addr[1]):
            self.current_player = 1 - self.current_player
            self.players[self.current_player].socket.send(f"{first_index},{second_index},{sign}".encode())

    def start(self) -> None:
        if not all(self.players):
            logger.error("Not enough players")
            return
        while True:
            current_player = self.players[self.current_player]
            data = current_player.socket.recv(1024)
            logger.info(data)
            if data:
                self.give_response(data)
            else:
                self.players[0].socket.close()
                self.players[1].socket.close()
                logger.info(f"{current_player.addr} disconnected")
                break

    def connect_player(self, player: Player) -> bool:
        if all(self.players):
            return False
        if self.players[0] is None:
            self.players[0] = player
        elif self.players[1] is None:
            self.players[1] = player
        return True


class Server:
    def __init__(self, ip: str, port: int) -> None:
        self.ip = ip
        self.port = port
        self.rooms: dict[str, Room] = dict()

    def create_room(self, conn: socket.socket, addr: Any, room_name: str, sign: int) -> Optional[Room]:
        if room_name in self.rooms:
            conn.send("101".encode())
            logger.error(f"Room already exists")
            return None
        self.rooms[room_name] = Room(room_name)
        player = Player(conn, addr)
        room = self.rooms[room_name]
        if sign == 1:
            room.players[0] = player
        if sign == -1:
            room.players[1] = player
        conn.send("202".encode())
        return room

    def connect_room(self, conn: socket.socket, addr: Any, room_name: str) -> Optional[Room]:
        if room_name not in self.rooms:
            conn.send("303".encode())
            logger.error(f"Room not exist")
            return None
        player = Player(conn, addr)
        room = self.rooms[room_name]
        if not room.connect_player(player):
            conn.send("103".encode())
            logger.error("Connection to full room")
            return None
        conn.send("202".encode())
        return room

    def room_command_handler(self, conn: socket.socket, addr: Any) -> Optional[Room]:
        response = conn.recv(1024).decode().split(",")
        if len(response) != 3:
            logger.error(f"Wrong command format f{response}")
            return None
        command, room_name, sign = response
        sign = int(sign)
        if command == "1":
            return self.create_room(conn, addr, room_name, sign)
        if command == "2":
            return self.connect_room(conn, addr, room_name)
        conn.send("301".encode())
        logger.error(f"Unexpected command {command}")
        return None

    def new_player_handler(self, conn: socket.socket, addr: Any) -> None:
        room = self.room_command_handler(conn, addr)
        if not room:
            return None
        while not all(room.players):
            time.sleep(0)
        logger.info(f"Room completed")
        if room.players[0].socket == conn and room.players[0].addr == addr:
            conn.sendall("1".encode())
        if room.players[1].socket == conn and room.players[1].addr == addr:
            conn.sendall("-1".encode())
        room.start()
        room_name = room.name
        del room
        logger.info(f"Room {room_name} close")

    def main(self) -> None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        logger.info(f"Server started at {self.ip}:{self.port}")
        sock.bind((self.ip, self.port))
        sock.listen()
        while True:
            conn, addr = sock.accept()
            logger.info(f"Connected from {addr}")
            thread = Thread(target=self.new_player_handler, args=(conn, addr))
            thread.start()


if __name__ == "__main__":
    server = Server("127.0.0.1", 8888)
    server.main()
