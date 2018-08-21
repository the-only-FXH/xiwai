#!/usr/bin/env python3
# coding = utf-8
import sys
sys.path.append("..")
from config import configfile
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    configfile.getConfig("database","DATABASE_URL"),
    encoding='utf-8',
    echo=False)
Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)
