var ContinuumView, VBox, VBoxForm, VBoxFormView, _, build_views,
  extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty;

_ = require("underscore");

build_views = require("../../common/build_views");

ContinuumView = require("../../common/continuum_view");

VBox = require("./vbox");

VBoxFormView = (function(superClass) {
  extend(VBoxFormView, superClass);

  function VBoxFormView() {
    return VBoxFormView.__super__.constructor.apply(this, arguments);
  }

  VBoxFormView.prototype.tagName = "form";

  VBoxFormView.prototype.attributes = {
    "class": "bk-widget-form",
    role: "form"
  };

  VBoxFormView.prototype.initialize = function(options) {
    VBoxFormView.__super__.initialize.call(this, options);
    this.views = {};
    return this.render();
  };

  VBoxFormView.prototype.render = function() {
    var child, children, i, key, len, ref, val;
    children = this.model.children();
    build_views(this.views, children);
    ref = this.views;
    for (key in ref) {
      if (!hasProp.call(ref, key)) continue;
      val = ref[key];
      val.$el.detach();
    }
    this.$el.empty();
    for (i = 0, len = children.length; i < len; i++) {
      child = children[i];
      this.$el.append("<br/");
      this.$el.append(this.views[child.id].$el);
    }
    return this;
  };

  return VBoxFormView;

})(ContinuumView);

VBoxForm = (function(superClass) {
  extend(VBoxForm, superClass);

  function VBoxForm() {
    return VBoxForm.__super__.constructor.apply(this, arguments);
  }

  VBoxForm.prototype.type = "VBoxForm";

  VBoxForm.prototype.default_view = VBoxFormView;

  VBoxForm.prototype.defaults = function() {
    return _.extend({}, VBoxForm.__super__.defaults.call(this), {
      children: []
    });
  };

  VBoxForm.prototype.children = function() {
    return this.get('children');
  };

  return VBoxForm;

})(VBox.Model);

module.exports = {
  Model: VBoxForm,
  View: VBoxFormView
};
