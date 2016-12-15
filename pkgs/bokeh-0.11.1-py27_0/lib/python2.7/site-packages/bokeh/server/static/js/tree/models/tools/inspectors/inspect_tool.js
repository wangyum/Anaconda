var Backbone, InspectTool, InspectToolListItemView, InspectToolView, Tool, _, inspect_tool_list_item_template,
  extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty;

_ = require("underscore");

Backbone = require("backbone");

Tool = require("../tool");

inspect_tool_list_item_template = require("./inspect_tool_list_item_template");

InspectToolListItemView = (function(superClass) {
  extend(InspectToolListItemView, superClass);

  function InspectToolListItemView() {
    return InspectToolListItemView.__super__.constructor.apply(this, arguments);
  }

  InspectToolListItemView.prototype.className = "bk-toolbar-inspector";

  InspectToolListItemView.prototype.template = inspect_tool_list_item_template;

  InspectToolListItemView.prototype.events = {
    'click [type="checkbox"]': '_clicked'
  };

  InspectToolListItemView.prototype.initialize = function(options) {
    this.listenTo(this.model, 'change:active', this.render);
    return this.render();
  };

  InspectToolListItemView.prototype.render = function() {
    this.$el.html(this.template(this.model.attrs_and_props()));
    return this;
  };

  InspectToolListItemView.prototype._clicked = function(e) {
    var active;
    active = this.model.get('active');
    return this.model.set('active', !active);
  };

  return InspectToolListItemView;

})(Backbone.View);

InspectToolView = (function(superClass) {
  extend(InspectToolView, superClass);

  function InspectToolView() {
    return InspectToolView.__super__.constructor.apply(this, arguments);
  }

  return InspectToolView;

})(Tool.View);

InspectTool = (function(superClass) {
  extend(InspectTool, superClass);

  function InspectTool() {
    return InspectTool.__super__.constructor.apply(this, arguments);
  }

  InspectTool.prototype.event_type = "move";

  InspectTool.prototype.nonserializable_attribute_names = function() {
    var attrs;
    attrs = _.without(InspectTool.__super__.nonserializable_attribute_names.call(this), 'active');
    return attrs.concat(['event_type', 'inner_only']);
  };

  InspectTool.prototype.bind_bokeh_events = function() {
    InspectTool.__super__.bind_bokeh_events.call(this);
    return this.listenTo(events, 'move', this._inspect);
  };

  InspectTool.prototype._inspect = function(vx, vy, e) {};

  InspectTool.prototype._exit_inner = function() {};

  InspectTool.prototype._exit_outer = function() {};

  InspectTool.prototype.defaults = function() {
    return _.extend({}, InspectTool.__super__.defaults.call(this), {
      inner_only: true,
      active: true,
      event_type: 'move'
    });
  };

  return InspectTool;

})(Tool.Model);

module.exports = {
  Model: InspectTool,
  View: InspectToolView,
  ListItemView: InspectToolListItemView
};
