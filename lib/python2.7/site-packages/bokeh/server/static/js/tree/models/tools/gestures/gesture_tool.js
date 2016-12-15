var ButtonTool, GestureTool, GestureToolButtonView, GestureToolView, _,
  extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty;

_ = require("underscore");

ButtonTool = require("../button_tool");

GestureToolButtonView = (function(superClass) {
  extend(GestureToolButtonView, superClass);

  function GestureToolButtonView() {
    return GestureToolButtonView.__super__.constructor.apply(this, arguments);
  }

  GestureToolButtonView.prototype._clicked = function() {
    var active;
    active = this.model.get('active');
    return this.model.set('active', !active);
  };

  return GestureToolButtonView;

})(ButtonTool.ButtonView);

GestureToolView = (function(superClass) {
  extend(GestureToolView, superClass);

  function GestureToolView() {
    return GestureToolView.__super__.constructor.apply(this, arguments);
  }

  return GestureToolView;

})(ButtonTool.View);

GestureTool = (function(superClass) {
  extend(GestureTool, superClass);

  function GestureTool() {
    return GestureTool.__super__.constructor.apply(this, arguments);
  }

  GestureTool.prototype.nonserializable_attribute_names = function() {
    return GestureTool.__super__.nonserializable_attribute_names.call(this).concat(['event_type', 'default_order']);
  };

  GestureTool.prototype.defaults = function() {
    return _.extend({}, GestureTool.__super__.defaults.call(this), {
      event_type: this.event_type,
      default_order: this.default_order
    });
  };

  return GestureTool;

})(ButtonTool.Model);

module.exports = {
  Model: GestureTool,
  View: GestureToolView,
  ButtonView: GestureToolButtonView
};
