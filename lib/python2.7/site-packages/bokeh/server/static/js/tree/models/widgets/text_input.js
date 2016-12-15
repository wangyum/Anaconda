var ContinuumView, InputWidget, TextInput, TextInputView, _, build_views, logger, template,
  extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty;

_ = require("underscore");

build_views = require("../../common/build_views");

ContinuumView = require("../../common/continuum_view");

logger = require("../../common/logging").logger;

template = require("./text_input_template");

InputWidget = require("./input_widget");

TextInputView = (function(superClass) {
  extend(TextInputView, superClass);

  function TextInputView() {
    return TextInputView.__super__.constructor.apply(this, arguments);
  }

  TextInputView.prototype.tagName = "div";

  TextInputView.prototype.attributes = {
    "class": "bk-widget-form-group"
  };

  TextInputView.prototype.template = template;

  TextInputView.prototype.events = {
    "change input": "change_input"
  };

  TextInputView.prototype.initialize = function(options) {
    TextInputView.__super__.initialize.call(this, options);
    this.render();
    return this.listenTo(this.model, 'change', this.render);
  };

  TextInputView.prototype.render = function() {
    this.$el.html(this.template(this.model.attributes));
    return this;
  };

  TextInputView.prototype.change_input = function() {
    var ref, value;
    value = this.$('input').val();
    logger.debug("widget/text_input: value = " + value);
    this.mset('value', value);
    return (ref = this.mget('callback')) != null ? ref.execute(this.model) : void 0;
  };

  return TextInputView;

})(ContinuumView);

TextInput = (function(superClass) {
  extend(TextInput, superClass);

  function TextInput() {
    return TextInput.__super__.constructor.apply(this, arguments);
  }

  TextInput.prototype.type = "TextInput";

  TextInput.prototype.default_view = TextInputView;

  TextInput.prototype.defaults = function() {
    return _.extend({}, TextInput.__super__.defaults.call(this), {
      value: "",
      title: ""
    });
  };

  return TextInput;

})(InputWidget.Model);

module.exports = {
  Model: TextInput,
  View: TextInputView
};
