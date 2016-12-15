var ActionTool, HelpTool, HelpToolView, _,
  extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty;

_ = require("underscore");

ActionTool = require("./action_tool");

HelpToolView = (function(superClass) {
  extend(HelpToolView, superClass);

  function HelpToolView() {
    return HelpToolView.__super__.constructor.apply(this, arguments);
  }

  HelpToolView.prototype["do"] = function() {
    return window.open(this.mget('redirect'));
  };

  return HelpToolView;

})(ActionTool.View);

HelpTool = (function(superClass) {
  extend(HelpTool, superClass);

  function HelpTool() {
    return HelpTool.__super__.constructor.apply(this, arguments);
  }

  HelpTool.prototype.default_view = HelpToolView;

  HelpTool.prototype.type = "HelpTool";

  HelpTool.prototype.tool_name = "Help";

  HelpTool.prototype.icon = "bk-tool-icon-help";

  HelpTool.prototype.initialize = function(attrs, options) {
    HelpTool.__super__.initialize.call(this, attrs, options);
    return this.register_property('tooltip', function() {
      return this.get('help_tooltip');
    });
  };

  HelpTool.prototype.defaults = function() {
    return _.extend({}, HelpTool.__super__.defaults.call(this), {
      help_tooltip: 'Click the question mark to learn more about Bokeh plot tools.',
      redirect: 'http://bokeh.pydata.org/en/latest/docs/user_guide/tools.html'
    });
  };

  return HelpTool;

})(ActionTool.Model);

module.exports = {
  Model: HelpTool,
  View: HelpToolView
};
