var Component, Layout, _,
  extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty;

_ = require("underscore");

Component = require("../component");

Layout = (function(superClass) {
  extend(Layout, superClass);

  function Layout() {
    return Layout.__super__.constructor.apply(this, arguments);
  }

  Layout.prototype.type = "Layout";

  Layout.prototype.defaults = function() {
    return _.extend({}, Layout.__super__.defaults.call(this), {
      width: null,
      height: null
    });
  };

  return Layout;

})(Component.Model);

module.exports = {
  Model: Layout
};
