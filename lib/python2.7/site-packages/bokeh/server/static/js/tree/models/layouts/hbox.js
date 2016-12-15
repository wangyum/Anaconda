var $, BaseBox, ContinuumView, HBox, HBoxView, _, build_views,
  extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty;

_ = require("underscore");

$ = require("jquery");

build_views = require("../../common/build_views");

ContinuumView = require("../../common/continuum_view");

BaseBox = require("./basebox");

HBoxView = (function(superClass) {
  extend(HBoxView, superClass);

  function HBoxView() {
    return HBoxView.__super__.constructor.apply(this, arguments);
  }

  HBoxView.prototype.tag = "div";

  HBoxView.prototype.attributes = {
    "class": "bk-hbox"
  };

  HBoxView.prototype.initialize = function(options) {
    HBoxView.__super__.initialize.call(this, options);
    this.views = {};
    this.render();
    return this.listenTo(this.model, 'change', this.render);
  };

  HBoxView.prototype.render = function() {
    var child, children, height, i, index, key, len, ref, val, width;
    children = this.model.children();
    build_views(this.views, children);
    ref = this.views;
    for (key in ref) {
      if (!hasProp.call(ref, key)) continue;
      val = ref[key];
      val.$el.detach();
    }
    this.$el.empty();
    width = this.mget("width");
    if (width != null) {
      this.$el.css({
        width: width + "px"
      });
    }
    height = this.mget("height");
    if (height != null) {
      this.$el.css({
        height: height + "px"
      });
    }
    for (index = i = 0, len = children.length; i < len; index = ++i) {
      child = children[index];
      this.$el.append(this.views[child.id].$el);
      if (index < children.length - 1) {
        this.$el.append($('<div class="bk-hbox-spacer"></div>'));
      }
    }
    return this;
  };

  return HBoxView;

})(ContinuumView);

HBox = (function(superClass) {
  extend(HBox, superClass);

  function HBox() {
    return HBox.__super__.constructor.apply(this, arguments);
  }

  HBox.prototype.type = "HBox";

  HBox.prototype.default_view = HBoxView;

  HBox.prototype.defaults = function() {
    return _.extend({}, HBox.__super__.defaults.call(this), {
      children: []
    });
  };

  HBox.prototype.children = function() {
    return this.get('children');
  };

  return HBox;

})(BaseBox.Model);

module.exports = {
  Model: HBox,
  View: HBoxView
};
