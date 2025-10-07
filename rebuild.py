# Modules
import sqlite3
import os
import re
import shutil
from typing import Callable
from itertools import count
from dataclasses import dataclass, field
from dotenv import load_dotenv

# --- Load .env file
load_dotenv() 

# --- Settings ---
@dataclass
class Console:
    id: int = field(init=False)
    name: str
    path: str
    db_params_class_type: int
    db_params_game_type: int
    games: list = field(init=False, default_factory=list)
    extensions: set = field(default_factory=set)

    def __post_init__(self):
        self.id = self.db_params_game_type


@dataclass
class Game:
    id: int = field(default_factory=count(1).__next__, init=False)
    name: str
    filename: str
    extension: str


@dataclass
class Settings:
    games_path: str = None
    games_path_stick: str = None
    db_path: str = None
    db_backup_path: str = None
    db_common_name: str = None
    db_games_name: str = None

    _working_directory: str = field(init=False)

    db_common_fullpath: str = field(init=False)
    db_common_backup_fullpath: str = field(init=False)
    db_games_fullpath: str = field(init=False)
    db_games_backup_fullpath: str = field(init=False)

    def __post_init__(self) -> None:
        self._working_directory = os.getcwd()

        self.db_common_fullpath = self.get_db_fullpath(db_filename=self.db_common_name)
        self.db_common_backup_fullpath = self.get_db_fullpath(
            db_filename=self.db_common_name, backup=True
        )
        self.db_games_fullpath = self.get_db_fullpath(db_filename=self.db_games_name)
        self.db_games_backup_fullpath = self.get_db_fullpath(
            db_filename=self.db_games_name, backup=True
        )

    def get_db_fullpath(self, db_filename: str, backup: bool = False) -> str:
        db_path = self.db_backup_path if backup else self.db_path
        return os.path.join(
            self._working_directory,
            db_path,
            db_filename,
        )


# --- Application --
@dataclass
class Application:
    settings: Settings = None
    consoles: list[Console] = field(init=False)

    def __post_init__(self) -> None:
        self.consoles = list()


# --- Files ---
class Files:

    @classmethod
    def change_filenames(cls, path: str):
        filenames = [
            f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))
        ]
        for filename in filenames:
            try:
                splitted = filename.split(".")
                name = ".".join(splitted[:-1])
                extension = splitted[-1]
            except ValueError as e:
                print("Unpack file {} error: {}".format(filename, e))

            new_name = re.sub(r"\(.*\)|\[.*\]", "", name).replace("_", " ").rstrip()
            os.rename(
                os.path.join(path, filename),
                os.path.join(path, "{}.{}".format(new_name, extension)),
            )

    @classmethod
    def get_filenames(cls, path: str):
        filenames = [
            f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))
        ]
        return filenames


# --- Database ---
class Database:

    def __init__(self, path: str, filename: str) -> None:
        self.path = path
        self.filename = filename
        self.__connection = None

    def __enter__(self) -> None:
        self.__connection = sqlite3.connect(os.path.join(self.path, self.filename))
        return self

    def __exit__(self, type, value, traceback) -> None:
        self.__connection.commit()
        self.__connection.close()

    @property
    def cursor(self) -> Callable:
        return self.__connection.cursor()

    def get_many(self, query: str) -> Callable:
        return self.cursor.execute(query).fetchall()

    def clear_table(self, table_name: str) -> None:
        return self.cursor.execute("DELETE FROM {}".format(table_name))


# --- Main ---
def main():

    # App init
    app = Application(
        Settings(
            games_path=os.getenv("GAMES_PATH"),
            games_path_stick=os.getenv("STICK_GAMES_PATH"),
            db_path=os.getenv("DB_PATH"),
            db_backup_path=os.getenv("DB_BACKUP_PATH"),
            db_common_name=os.getenv("DB_COMMON_NAME"),
            db_games_name=os.getenv("DB_GAMES_NAME"),
        )
    )

    # Consoles
    # NES
    app.consoles += [
        Console(
            name="NES",
            path="fc",
            db_params_class_type=1,
            db_params_game_type=1,
            extensions={".nes"}
        ),
        Console(
            name="MD",
            path="md",
            db_params_class_type=5,
            db_params_game_type=5,
            extensions={".bin", ".smd", ".md"}
        ),
        Console(
            name="CPS",
            path="cps",
            db_params_class_type=0,
            db_params_game_type=0,
            extensions={".zip"}
        ),
        Console(
            name="SFC",
            path="sfc",
            db_params_class_type=6,
            db_params_game_type=6,
            extensions={".smc", ".sfc", ".fig"}
        ),
        Console(
            name="GB",
            path="gb",
            db_params_class_type=2,
            db_params_game_type=7,
            extensions={".gb"}
        ),
        Console(
            name="GBC",
            path="gbc",
            db_params_class_type=4,
            db_params_game_type=7,
            extensions={".gbc"}
        ),
        Console(
            name="GBA",
            path="gba",
            db_params_class_type=3,
            db_params_game_type=7,
            extensions={".gba"}
        ),
        Console(
            name="PS1",
            path="ps1",
            db_params_class_type=4,
            db_params_game_type=9,
            extensions={".iso", ".img"}
        ),
    ]

    # Create a DB backup directory
    if not os.path.exists(app.settings.db_backup_path):
        os.mkdir(app.settings.db_backup_path)

    # Delete existing DB backups
    for db_path in (
        app.settings.db_common_backup_fullpath,
        app.settings.db_games_backup_fullpath,
    ):
        if os.path.exists(db_path):
            os.remove(db_path)

    # Create DB backups
    shutil.copyfile(
        app.settings.db_common_fullpath, app.settings.db_common_backup_fullpath
    )
    shutil.copyfile(
        app.settings.db_games_fullpath, app.settings.db_games_backup_fullpath
    )

    # Clear DB tables
    with Database(app.settings.db_path, app.settings.db_games_name) as db:
        db_tables = (
            "tbl_en",
            "tbl_game",
            "tbl_ko",
            "tbl_match",
            "tbl_path",
            "tbl_total",
            "tbl_tw",
            "tbl_video",
            "tbl_zh",
        )
        for db_table in db_tables:
            db.clear_table(db_table)

    with Database(app.settings.db_path, app.settings.db_common_name) as db:
        db_tables = (
            "GameInfo",
            "History",
        )
        for db_table in db_tables:
            db.clear_table(db_table)

    # Process consoles and games
    for console in app.consoles:
        console_game_path = os.path.join(app.settings.games_path, console.path)
        console_game_path_stick = os.path.join(app.settings.games_path_stick, console.path)
        Files.change_filenames(console_game_path)
        filenames: list = Files.get_filenames(console_game_path)
        for filename in filenames:
            filename_parts = filename.split(".")
            file_extension = f".{filename_parts[1]}"
            if file_extension in console.extensions:
                console.games.append(
                    Game(filename_parts[0], filename, file_extension)
                )

        # Table: tbl_en
        with Database(app.settings.db_path, app.settings.db_games_name) as db:
            for game in console.games:
                db.cursor.execute(
                    'INSERT INTO tbl_en (en_id, en_title) VALUES ({}, "{}")'.format(
                        game.id, game.name
                    )
                )
                db.cursor.execute(
                    'INSERT INTO tbl_ko (ko_id, ko_title) VALUES ({}, "{}")'.format(
                        game.id, game.name
                    )
                )
                db.cursor.execute(
                    'INSERT INTO tbl_match (ID, zh_match) VALUES ({}, "{}")'.format(
                        game.id, game.name
                    )
                )
                db.cursor.execute(
                    'INSERT INTO tbl_tw (tw_id, tw_title) VALUES ({}, "{}")'.format(
                        game.id, game.name
                    )
                )
                db.cursor.execute(
                    'INSERT INTO tbl_zh (zh_id, zh_title) VALUES ({}, "{}")'.format(
                        game.id, game.name
                    )
                )
                db.cursor.execute(
                    'INSERT INTO tbl_video (video_id, path_id) VALUES ({}, {})'.format(
                        game.id, 1
                    )
                )

                db.cursor.execute(
                    f'INSERT INTO tbl_game (gameid, game, suffix, zh_id, en_id, ko_id, video_id, class_type, game_type, hard, timer) VALUES ( \
                        {game.id}, "{game.name}", "{game.extension}", {game.id}, {game.id}, {game.id}, {game.id}, {console.db_params_class_type}, {console.db_params_game_type}, 0, "{console_game_path_stick}")'
                )

    with Database(app.settings.db_path, app.settings.db_games_name) as db:
        db.cursor.execute(
            f'INSERT INTO tbl_path (path_id, path) VALUES (1, "{app.settings.games_path_stick}")'
        )

        games_total = db.cursor.execute(
            "SELECT COUNT(*) FROM tbl_en"
        ).fetchone()[0]
        
        db.cursor.execute(
            f'INSERT INTO tbl_total (ID, total) VALUES ({games_total}, {games_total})'
        )

if __name__ == "__main__":
    main()
