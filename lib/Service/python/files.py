import os
import fnmatch
import db


"""
/**
 * @copyright 2021 Andrey Borysenko <andrey18106x@gmail.com>
 * @copyright 2021 Alexander Piskun <bigcat88@icloud.com>
 *
 * @author 2021 Alexander Piskun <bigcat88@icloud.com>
 *
 * @license GNU AGPL version 3 or any later version
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */
"""


StoragesInfo = []


def get_file_data(file_info: dict, data_dir: str, remote_filesize_limit: int) -> bytes:
    direct = can_directly_access_file(file_info)
    while direct:
        full_path = get_file_full_path(data_dir, file_info['storage'], file_info['path'])
        if not full_path:
            break
        h_file = None
        data = bytes(b'')
        try:
            h_file = open(full_path, "rb")
            data = h_file.read()
        except OSError:                     # if we can open file, and exception during read of file - ignore file.
            if h_file is None:              # we want only require file from php if we cant open it.
                break
        finally:
            if h_file is not None:
                h_file.close()
        return data
    if file_info['size'] > remote_filesize_limit:
        return b''
    return request_file_from_php(file_info)


def request_file_from_php(file_info: dict) -> bytes:
    user_id = get_storage_user_id(file_info['storage'])
    if not len(user_id):
        return bytes(b'')
    success, err_or_data = db.occ_call('mediadc:tasks:filecontents', str(file_info['fileid']), user_id, decode=False)
    if not success:
        print('get_file_data:', err_or_data)
        return bytes(b'')
    return err_or_data


def get_file_full_path(data_dir: str, storage_id: int, relative_path: str) -> str:
    mount_point = get_storage_mount_point(storage_id)
    if not mount_point:
        return ''
    return data_dir + mount_point + relative_path


def can_directly_access_file(file_info: dict) -> bool:
    if file_info['encrypted'] == 1:
        return False
    storage_info = get_storage_info(file_info['storage'])
    if not storage_info:
        return False
    if storage_info['available'] == 0:
        return False
    if storage_info.get('storage_backend') is None:
        storage_txt_id = storage_info['id']
        supported_start_list = ('local::', 'home::')
        if storage_txt_id.startswith(supported_start_list):
            return True
    return False


def update_storages_info():
    global StoragesInfo
    StoragesInfo = db.get_all_storage_info()


def get_storage_info(storage_id: int):
    for x in StoragesInfo:
        if x['numeric_id'] == storage_id:
            return x
    return {}


def get_storage_mount_point(storage_id: int) -> str:
    for x in StoragesInfo:
        if x['numeric_id'] == storage_id:
            return x['mount_point']
    return ''


def get_storage_user_id(storage_id: int) -> str:
    for x in StoragesInfo:
        if x['numeric_id'] == storage_id:
            return x['user_id']
    return ''


def is_path_in_exclude(path: str, exclude: list) -> bool:
    name = os.path.basename(path)
    for e in exclude:
        if fnmatch.fnmatch(name, e):
            return True
    return False
