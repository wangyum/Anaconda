var TableWidget, Widget, _,
  extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty;

_ = require("underscore");

Widget = require("./widget");

TableWidget = (function(superClass) {
  extend(TableWidget, superClass);

  function TableWidget() {
    return TableWidget.__super__.constructor.apply(this, arguments);
  }

  TableWidget.prototype.type = "TableWidget";

  TableWidget.prototype.defaults = function() {
    return _.extend({}, TableWidget.__super__.defaults.call(this), {
      source: null
    });
  };

  return TableWidget;

})(Widget.Model);

module.exports = {
  Model: TableWidget
};
