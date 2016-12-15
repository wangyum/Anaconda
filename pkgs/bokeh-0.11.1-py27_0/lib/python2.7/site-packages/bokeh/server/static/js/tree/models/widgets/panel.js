var $, ContinuumView, Panel, PanelView, Widget, _,
  extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty;

_ = require("underscore");

$ = require("jquery");

ContinuumView = require("../../common/continuum_view");

Widget = require("./widget");

PanelView = (function(superClass) {
  extend(PanelView, superClass);

  function PanelView() {
    return PanelView.__super__.constructor.apply(this, arguments);
  }

  PanelView.prototype.initialize = function(options) {
    PanelView.__super__.initialize.call(this, options);
    return this.render();
  };

  PanelView.prototype.render = function() {
    this.$el.empty();
    return this;
  };

  return PanelView;

})(ContinuumView);

Panel = (function(superClass) {
  extend(Panel, superClass);

  function Panel() {
    return Panel.__super__.constructor.apply(this, arguments);
  }

  Panel.prototype.type = "Panel";

  Panel.prototype.default_view = PanelView;

  Panel.prototype.defaults = function() {
    return _.extend({}, Panel.__super__.defaults.call(this), {
      title: "",
      child: null,
      closable: false
    });
  };

  return Panel;

})(Widget.Model);

module.exports = {
  Model: Panel,
  View: PanelView
};
