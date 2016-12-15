var $, BaseBox, ContinuumView, VBox, VBoxView, _, build_views,
  extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty;

_ = require("underscore");

$ = require("jquery");

build_views = require("../../common/build_views");

ContinuumView = require("../../common/continuum_view");

BaseBox = require("./basebox");

VBoxView = (function(superClass) {
  extend(VBoxView, superClass);

  function VBoxView() {
    return VBoxView.__super__.constructor.apply(this, arguments);
  }

  VBoxView.prototype.tag = "div";

  VBoxView.prototype.attributes = {
    "class": "bk-vbox"
  };

  VBoxView.prototype.initialize = function(options) {
    VBoxView.__super__.initialize.call(this, options);
    this.views = {};
    this.render();
    return this.listenTo(this.model, 'change', this.render);
  };

  VBoxView.prototype.render = function() {
    var child, children, height, i, key, len, ref, spacer, spacer_height, val, width;
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
      spacer_height = height / (children.length * 2);
    } else {
      spacer_height = 20;
    }
    spacer = $('<div>').addClass('bk-vbox-spacer').css({
      height: spacer_height
    });
    this.$el.append($(spacer));
    for (i = 0, len = children.length; i < len; i++) {
      child = children[i];
      this.$el.append(this.views[child.id].$el);
      this.$el.append($(spacer));
    }
    return this;
  };

  return VBoxView;

})(ContinuumView);

VBox = (function(superClass) {
  extend(VBox, superClass);

  function VBox() {
    return VBox.__super__.constructor.apply(this, arguments);
  }

  VBox.prototype.type = "VBox";

  VBox.prototype.default_view = VBoxView;

  VBox.prototype.defaults = function() {
    return _.extend({}, VBox.__super__.defaults.call(this), {
      children: []
    });
  };

  VBox.prototype.children = function() {
    return this.get('children');
  };

  return VBox;

})(BaseBox.Model);

module.exports = {
  Model: VBox,
  View: VBoxView
};
