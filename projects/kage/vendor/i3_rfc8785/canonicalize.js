'use strict';

module.exports = function (object) {
    var buffer = '';
    serialize(object);
    return buffer;

    function serialize(object) {
        if (object === null || typeof object !== 'object') {
            buffer += JSON.stringify(object);
        } else if (Array.isArray(object)) {
            buffer += '[';
            let next = false;
            object.forEach((element) => {
                if (next) {
                    buffer += ',';
                }
                next = true;
                serialize(element);
            });
            buffer += ']';
        } else {
            buffer += '{';
            let next = false;
            Object.keys(object).sort().forEach((property) => {
                if (next) {
                    buffer += ',';
                }
                next = true;
                serialize(property);
                buffer += ':';
                serialize(object[property]);
            });
            buffer += '}';
        }
    }
};
