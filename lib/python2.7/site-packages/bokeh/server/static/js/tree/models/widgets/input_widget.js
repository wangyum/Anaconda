var InputWidget, Widget, _,
  extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty;

_ = require("underscore");

Widget = require("./widget");

InputWidget = (function(superClass) {
  extend(InputWidget, superClass);

  function InputWidget() {
    return InputWidget.__super__.constructor.apply(this, arguments);
  }

  InputWidget.prototype.type = "InputWidget";

  InputWidget.prototype.defaults = function() {
    return _.extend({}, InputWidget.__super__.defaults.call(this), {
      callback: null,
      title: ""
    });
  };

  return InputWidget;

})(Widget.Model);

module.exports = {
  Model: InputWidget
};
