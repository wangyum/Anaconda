var AbstractButton, ContinuumView, Toggle, ToggleView, _,
  extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty;

_ = require("underscore");

ContinuumView = require("../../common/continuum_view");

AbstractButton = require("./abstract_button");

ToggleView = (function(superClass) {
  extend(ToggleView, superClass);

  function ToggleView() {
    return ToggleView.__super__.constructor.apply(this, arguments);
  }

  ToggleView.prototype.tagName = "button";

  ToggleView.prototype.events = {
    "click": "change_input"
  };

  ToggleView.prototype.initialize = function(options) {
    ToggleView.__super__.initialize.call(this, options);
    this.render();
    return this.listenTo(this.model, 'change', this.render);
  };

  ToggleView.prototype.render = function() {
    var icon, key, label, ref, val;
    icon = this.mget('icon');
    if (icon != null) {
      build_views(this.views, [icon]);
      ref = this.views;
      for (key in ref) {
        if (!hasProp.call(ref, key)) continue;
        val = ref[key];
        val.$el.detach();
      }
    }
    this.$el.empty();
    this.$el.addClass("bk-bs-btn");
    this.$el.addClass("bk-bs-btn-" + this.mget("type"));
    if (this.mget("disabled")) {
      this.$el.attr("disabled", "disabled");
    }
    label = this.mget("label");
    if (icon != null) {
      this.$el.append(this.views[icon.id].$el);
      label = " " + label;
    }
    this.$el.append(document.createTextNode(label));
    if (this.mget("active")) {
      this.$el.addClass("bk-bs-active");
    }
    this.$el.attr("data-bk-bs-toggle", "button");
    return this;
  };

  ToggleView.prototype.change_input = function() {
    var ref;
    this.mset('active', !this.mget('active'));
    return (ref = this.mget('callback')) != null ? ref.execute(this.model) : void 0;
  };

  return ToggleView;

})(ContinuumView);

Toggle = (function(superClass) {
  extend(Toggle, superClass);

  function Toggle() {
    return Toggle.__super__.constructor.apply(this, arguments);
  }

  Toggle.prototype.type = "Toggle";

  Toggle.prototype.default_view = ToggleView;

  Toggle.prototype.defaults = function() {
    return _.extend({}, Toggle.__super__.defaults.call(this), {
      active: false,
      label: "Toggle"
    });
  };

  return Toggle;

})(AbstractButton.Model);

module.exports = {
  Model: Toggle,
  View: ToggleView
};
