from enum import Enum
from pydantic import BaseModel
from typing import Optional

class SharePermissions(int, Enum):
    read = 0
    create = 1
    update = 2
    delete = 4

class Login(BaseModel):
    username: str
    password: Optional[str] = None
    digest: Optional[str] = None
    passworddigest: Optional[str] = None
    getauth: Optional[int] = 1
    logout: Optional[int] = 1

class Folder(BaseModel):
    auth: str
    folderid: Optional[int] = None
    path: Optional[str] = None
    recursive: Optional[int] = None
    showdeleted: Optional[int] = None
    nofiles: Optional[int] = None
    noshares: Optional[int] = None

class FolderCreate(Folder):
    name: Optional[str] = None

class FolderUpdate(Folder):
    tofolderid: Optional[int] = None
    topath: Optional[str] = None
    noover: Optional[int] = None
    skipexisting: Optional[int] = None
    copycontentonly: Optional[int] = None

class File(BaseModel):
    auth: str
    folderid: Optional[int] = None
    fileid: Optional[int] = None
    path: Optional[str] = None
    filename: Optional[str] = None
    nopartial: Optional[int] = 1
    progresshash: Optional[str] = None
    renameifexists: Optional[int] = None
    mtime: Optional[int] = None
    ctime: Optional[int] = None

class FileUpdate(File):
    tofolderid: Optional[int] = None
    topath: Optional[str] = None
    toname: Optional[str] = None
    noover: Optional[int] = None
    mtime: Optional[int] = None
    ctime: Optional[int] = None

class Share(BaseModel):
    shareid: Optional[int] = None
    folderid: Optional[int] = None
    path: Optional[str] = None
    mail: str
    permissions: SharePermissions
    name: Optional[str] = None
    message: Optional[str] = None

class ShareList(BaseModel):
    norequests: Optional[int] = None
    noshares: Optional[int] = None
    noincoming: Optional[int] = None
    nooutgoing: Optional[int] = None