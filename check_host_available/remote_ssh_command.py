#!/usr/bin/python3
# -*- encoding:utf-8 -*-
# Author: lele,wanx
# Date: 2022-03-15 14:05:54
# Last Modified by:   lele,wanx
# Last Modified time: 2022-03-15 14:05:54

import paramiko
from paramiko.ssh_exception import AuthenticationException,\
    SSHException, NoValidConnectionsError
import time, socket


class Remote_SSH_Server():
    """
    Provide remote ssh service. The main methods included are:
    connect, ssh_open, sftp_open, send_ssh_command, transport_file.
    Also supported with.
    """

    def __init__(self, **host: dict) -> None:
        self.ip = host.get("ip")
        self.port = host.get("port")
        self.username = host.get("username")
        self.password = host.get("password")
        self.ssh_client = None
        self.sftp_client = None
        self._transport = None

    def __enter__(self):
        self.connect()
        return self

    def connect(self):
        try:
            self._transport = paramiko.Transport((self.ip, self.port))
            self._transport.connect(username=self.username,
                                    password=self.password)
            return True
        except AuthenticationException as e:
            print(f"AuthenticationException. {e}")
        except SSHException as e:
            print(f"SSHException . {e}")
        except NoValidConnectionsError as e:
            print(f"NoValidConnectionsError. {e}")

    def ssh_open(self):
        if self.connect():
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client._transport = self._transport
            self.ssh_client.set_missing_host_key_policy(
                paramiko.AutoAddPolicy())
            return True

    def sftp_open(self):
        self.sftp_client = paramiko.SFTPClient.from_transport(self._transport)
        return True

    def send_ssh_command(self, command, sudo=False):
        if sudo:
            command = f"echo {self.password} | sudo -S {command}"
        stdout, stderr = self.ssh_client.exec_command(command)[1:]
        return_string = ''
        for line in iter(stdout.readline, ""):
            return_string += line
        for line in iter(stderr.readline, ""):
            return_string += line
        code_number = stdout.channel.recv_exit_status()
        return code_number, return_string

    def transport_file(self, localpathfile, remotepathfile, mode="put"):
        if mode == "put":
            self.sftp_client.put(localpathfile, remotepathfile)
        elif mode == "get":
            self.sftp_client.get(remotepathfile, localpathfile)
        else:
            print(f"mode args error.")

    def __exit__(self, exc_type, exc_value, exc_tb):
        if all([exc_value is None, exc_type is None, exc_tb is None]):
            pass
        else:
            print(
                f"\nexc_type: {exc_type}, \nexc_value: {exc_value}, \nexc_tb: {exc_tb}"
            )
        if self.ssh_client:
            self.ssh_client.close()
        if self.sftp_client:
            self.sftp_client.close()
        if self._transport:
            self._transport.close()
