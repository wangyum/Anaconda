var $, $1, ActionTool, PreviewSaveTool, PreviewSaveToolView, _, preview_save_tool_template,
  extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty;

_ = require("underscore");

$ = require("jquery");

$1 = require("bootstrap/modal");

ActionTool = require("./action_tool");

preview_save_tool_template = require("./preview_save_tool_template");

PreviewSaveToolView = (function(superClass) {
  extend(PreviewSaveToolView, superClass);

  function PreviewSaveToolView() {
    return PreviewSaveToolView.__super__.constructor.apply(this, arguments);
  }

  PreviewSaveToolView.prototype.className = "bk-bs-modal";

  PreviewSaveToolView.prototype.template = preview_save_tool_template;

  PreviewSaveToolView.prototype.initialize = function(options) {
    PreviewSaveToolView.__super__.initialize.call(this, options);
    return this.render();
  };

  PreviewSaveToolView.prototype.render = function() {
    this.$el.empty();
    this.$el.html(this.template());
    this.$el.attr("tabindex", "-1");
    this.$el.on('hidden', (function(_this) {
      return function() {
        return _this.$el.modal('hide');
      };
    })(this));
    return this.$el.modal({
      show: false
    });
  };

  PreviewSaveToolView.prototype["do"] = function() {
    var canvas;
    canvas = this.plot_view.canvas_view.canvas[0];
    this.$('.bk-bs-modal-body img').attr("src", canvas.toDataURL());
    return this.$el.modal('show');
  };

  return PreviewSaveToolView;

})(ActionTool.View);

PreviewSaveTool = (function(superClass) {
  extend(PreviewSaveTool, superClass);

  function PreviewSaveTool() {
    return PreviewSaveTool.__super__.constructor.apply(this, arguments);
  }

  PreviewSaveTool.prototype.default_view = PreviewSaveToolView;

  PreviewSaveTool.prototype.type = "PreviewSaveTool";

  PreviewSaveTool.prototype.tool_name = "Preview/Save";

  PreviewSaveTool.prototype.icon = "bk-tool-icon-save";

  return PreviewSaveTool;

})(ActionTool.Model);

module.exports = {
  Model: PreviewSaveTool,
  View: PreviewSaveToolView
};
