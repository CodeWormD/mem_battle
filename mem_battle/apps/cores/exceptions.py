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


class CommentHasBeenDeleted(CommentDoesNotExist):
    default_detail = ('Comment deleted. You can not update it')


class TagDoesNotExist(CommentDoesNotExist):
    default_detail = ('Tag does not exist.')


class BattleForMemsEnd(APIException):
    status_code = status.HTTP_204_NO_CONTENT
    default_detail = ('BattleForMemsEnd. You have battled all mems')
    default_code = 'no_content'


class QuersetBattleError(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = ('QuersetBattleError. Smth wrong with mem battle get_queryset')
    default_code = 'not_found'


class QuerysetError(APIException):
    status_code = status.HTTP_204_NO_CONTENT
    default_detail = ('QuerySetError in get_random_mems or maybe you have seen all mems')
    default_code = 'no_content'


class ProfileNotExistsError(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = ('There is not such profile')
    default_code = 'not_found'


class FollowyourselfError(APIException):
    status_code = status.HTTP_204_NO_CONTENT
    default_detail = ('You can not follow yourself')
    default_code = 'no_content'


class FollowerDuplicationError(APIException):
    status_code = status.HTTP_204_NO_CONTENT
    default_detail = ('You can not follow twice one person')
    default_code = 'no_content'