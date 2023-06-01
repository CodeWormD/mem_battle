from rest_framework import status
from rest_framework.exceptions import APIException


class UserDoesNotExist(Exception):
    pass


class UserAlreadyVerified(Exception):
    pass


class MailSendingException(Exception):
    pass


class MemDoesNotExist(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = ('Mem does not exist.')
    default_code = 'not_found'


class MemListError(MemDoesNotExist):
    default_detail = ('Can not get list of mems')


class CommentDoesNotExist(MemDoesNotExist):
    default_detail = ('Comment does not exist.')


class CommentListDoesNotExists(CommentDoesNotExist):
    default_detail = ('Can not get list of comments')


class TagDoesNotExist(CommentDoesNotExist):
    default_detail = ('Tag does not exist.')