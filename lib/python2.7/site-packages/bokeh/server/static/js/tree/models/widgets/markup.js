var Markup, Widget,
  extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty;

Widget = require("./widget");

Markup = (function(superClass) {
  extend(Markup, superClass);

  function Markup() {
    return Markup.__super__.constructor.apply(this, arguments);
  }

  Markup.prototype.type = "Markup";

  return Markup;

})(Widget.Model);

module.exports = {
  Model: Markup
};
