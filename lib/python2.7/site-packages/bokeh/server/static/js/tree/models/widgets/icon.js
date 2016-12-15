var AbstractIcon, ContinuumView, Icon, IconView, _,
  extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty;

_ = require("underscore");

ContinuumView = require("../../common/continuum_view");

AbstractIcon = require("./abstract_icon");

IconView = (function(superClass) {
  extend(IconView, superClass);

  function IconView() {
    return IconView.__super__.constructor.apply(this, arguments);
  }

  IconView.prototype.tagName = "i";

  IconView.prototype.initialize = function(options) {
    IconView.__super__.initialize.call(this, options);
    this.render();
    return this.listenTo(this.model, 'change', this.render);
  };

  IconView.prototype.render = function() {
    var flip, size;
    this.$el.empty();
    this.$el.addClass("bk-fa");
    this.$el.addClass("bk-fa-" + this.mget("icon_name"));
    size = this.mget("size");
    if (size != null) {
      this.$el.css({
        "font-size": size + "em"
      });
    }
    flip = this.mget("flip");
    if (flip != null) {
      this.$el.addClass("bk-fa-flip-" + flip);
    }
    if (this.mget("spin")) {
      this.$el.addClass("bk-fa-spin");
    }
    return this;
  };

  return IconView;

})(ContinuumView);

Icon = (function(superClass) {
  extend(Icon, superClass);

  function Icon() {
    return Icon.__super__.constructor.apply(this, arguments);
  }

  Icon.prototype.type = "Icon";

  Icon.prototype.default_view = IconView;

  Icon.prototype.defaults = function() {
    return _.extend({}, Icon.__super__.defaults.call(this), {
      icon_name: "check",
      size: null,
      flip: null,
      spin: false
    });
  };

  return Icon;

})(AbstractIcon.Model);

module.exports = {
  Model: Icon,
  View: IconView
};
