from blockchainetl_common.executors.retriable_value_error import RetriableValueError
from jsonrpcclient.exceptions import JsonRpcClientError, ReceivedNon2xxResponseError
from pyzil.zilliqa.api import APIError
from requests.exceptions import Timeout as RequestsTimeout, HTTPError, TooManyRedirects

RETRY_EXCEPTIONS = (ConnectionError, HTTPError, RequestsTimeout, TooManyRedirects, OSError, RetriableValueError, JsonRpcClientError, ReceivedNon2xxResponseError, APIError)
