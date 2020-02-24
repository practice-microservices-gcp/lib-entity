import re

def serializable(Cls):
    class Entity(Cls):
        def _element_to_json(self, obj):
            classPattern = re.compile("^<class 'entity_decorator.*")
            listPatter = re.compile("^<class 'list.*")
            jsonStr = ""
            typeObj = str(type(obj))

            if classPattern.match(typeObj):
                dic = vars(obj)
                keys = list(dic)
                leng = len(keys)

                for index in range(leng):
                    typeItem = str(type(dic[keys[index]]))

                    if classPattern.match(typeItem):
                        tupla = "\"{key}\":{value}".format(
                            key=keys[index], value=dic[keys[index]].to_json())
                    elif listPatter.match(typeItem):
                        tupla = "\"{key}\":{value}".format(
                            key=keys[index], value=self._json_list(dic[keys[index]]))
                    else:
                        tupla = "\"{key}\":{value}".format(
                            key=keys[index], value=dic[keys[index]])

                    if index != (leng - 1):
                        jsonStr += tupla + ","
                    else:
                        jsonStr += tupla

                jsonStr = "{" + jsonStr + "}"
            elif listPatter.match(typeObj):
                jsonStr = self._json_list(obj)
            else:
                jsonStr = "\"" + str(obj) + "\""

            return jsonStr

        def _json_list(self, elements):
            jsonStr = ""
            leng = len(elements)
            classPattern = re.compile("^<class 'entity_decorator.*")

            for index in range(leng):
                typeItem = str(type(elements[index]))

                if classPattern.match(typeItem):
                    tupla = elements[index].to_json()
                else:
                    tupla = self._element_to_json(elements[index])

                if index != (leng - 1):
                    jsonStr += tupla + ","
                else:
                    jsonStr += tupla

            return "[" + jsonStr + "]"

        def to_json(self):
            dic = self.__dict__
            keys = list(dic)
            leng = len(keys)

            jsonStr = ""

            for index in range(leng):
                tupla = "\"{key}\":{value}".format(
                    key=keys[index], value=self._element_to_json(getattr(self, keys[index])))

                if index != (leng - 1):
                    jsonStr += tupla + ","
                else:
                    jsonStr += tupla

            return "{" + jsonStr + "}"

    return Entity
