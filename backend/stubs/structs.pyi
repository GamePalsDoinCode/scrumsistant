from typing import Any, Callable, Dict, List, Optional, TypeVar, Union, overload

T = TypeVar('T')

class UserInfo:
    @overload
    def serialize(
        self: 'UserInfo',
        skip_list: Optional[List[str]],
        serialize_method: Callable[[Dict[Any, Any]], Dict[str, Union[str, int, bool]]],
    ) -> Dict[str, Union[str, int, bool]]: ...
    @overload
    def serialize(
        self: 'UserInfo', skip_list: Optional[List[str]], serialize_method: Callable[[Dict[Any, Any]], T]
    ) -> T: ...
