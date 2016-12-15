var BaseBox, Layout, _,
  extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty;

_ = require("underscore");

Layout = require("./layout");

BaseBox = (function(superClass) {
  extend(BaseBox, superClass);

  function BaseBox() {
    return BaseBox.__super__.constructor.apply(this, arguments);
  }

  BaseBox.prototype.type = "BaseBox";

  BaseBox.prototype.defaults = function() {
    return _.extend({}, BaseBox.__super__.defaults.call(this), {
      width: null,
      height: null
    });
  };

  return BaseBox;

})(Layout.Model);

module.exports = {
  Model: BaseBox
};
