from abc import abstractmethod, ABC

from vse.core.maps import ACTION_MAP
from vse.core.exceptions import MappingAgentError
from vse.handlers import HandlerResult, Handler, DefaultHandler, ParamsSchema

from vse.core.task import VSETask
from vse.core.exceptions import InvalidHandlerErr


class IMapper(ABC):

    @abstractmethod
    def get_handler(self, task: VSETask) -> Handler:
        pass


class MapAgent:

    def __init__(self, **kwargs):
        self.map = kwargs.get("map", {})
        self.schema = None


class VSEMapAgent(MapAgent):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def add_handler(self, h_name, handler, params_schema):
        """Adds new Handler to the Map"""
        try:
            if not issubclass(handler, Handler):
                raise MappingAgentError("Must be the class, if param is of type Handler, resubmit without '()' ")

            if not isinstance(params_schema, ParamsSchema):
                raise MappingAgentError("Must be of type ParamsSchema")

            self.map[h_name] = {}
            self.map[h_name]['handler'] = handler
            self.map[h_name]['params_schema'] = params_schema
            return True
        except Exception:

            raise MappingAgentError(
                "Must register using Class for example MA.add_handler(Handler, ParamsSchema), resubmit without '()' ")

    def get_handler(self, h_name):
        """returns the requested handler"""
        return self.map.get(h_name)

    def get_handler_count(self):
        """returns total count of current handlers in the map"""
        return len(self.map)

    def delete_handler(self, h_name):
        result = self.map.get(h_name)
        if result:
            del self.map[h_name]
            return True

        return False

    def update(self, h_name, handler, params_schema):
        try:
            self.map[h_name]['handler'] = handler
            self.map[h_name]['params_schema'] = params_schema
            return True

        except KeyError:
            return False


class VSEActionMapper(IMapper):

    def __init__(self):
        self.action_map = ACTION_MAP

    def get_handler(self, task: VSETask) -> Handler:
        """
        Queries the HandlerMap based on the VSETask.action param. If Action is not found, a default Handler
        is returned.

        """
        if isinstance(task, VSETask):
            action = self.action_map.get(task.action, self.action_map.get("default"))

            handler_class = action.get("handler")

            if issubclass(handler_class, DefaultHandler):
                raise InvalidHandlerErr(f"Invalid Handler, Supported Handlers: '{self.action_map.keys()}'")

            handler = handler_class(
                name=task.action,
                params=task.params,
                task=task,
                params_schema=action.get("params_schema")()
            )
            return handler

        raise InvalidHandlerErr("Invalid Type provided, Must be of type Handler()")
