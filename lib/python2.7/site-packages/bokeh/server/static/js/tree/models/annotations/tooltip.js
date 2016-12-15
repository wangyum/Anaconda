var $, Annotation, PlotWidget, Tooltip, TooltipView, _, logger,
  extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty;

$ = require("jquery");

_ = require("underscore");

Annotation = require("./annotation");

PlotWidget = require("../../common/plot_widget");

logger = require("../../common/logging").logger;

TooltipView = (function(superClass) {
  extend(TooltipView, superClass);

  function TooltipView() {
    return TooltipView.__super__.constructor.apply(this, arguments);
  }

  TooltipView.prototype.className = "bk-tooltip";

  TooltipView.prototype.initialize = function(options) {
    TooltipView.__super__.initialize.call(this, options);
    this.$el.appendTo(this.plot_view.$el.find('div.bk-canvas-overlays'));
    this.$el.css({
      'z-index': 1010
    });
    return this.$el.hide();
  };

  TooltipView.prototype.bind_bokeh_events = function() {
    return this.listenTo(this.model, 'change:data', this._draw_tips);
  };

  TooltipView.prototype.render = function() {
    return this._draw_tips();
  };

  TooltipView.prototype._draw_tips = function() {
    var arrow_width, content, i, left, len, ow, ref, side, sx, sy, tip, top, val, vx, vy;
    this.$el.empty();
    this.$el.hide();
    this.$el.toggleClass("bk-tooltip-custom", this.mget("custom"));
    if (_.isEmpty(this.mget('data'))) {
      return;
    }
    ref = this.mget('data');
    for (i = 0, len = ref.length; i < len; i++) {
      val = ref[i];
      vx = val[0], vy = val[1], content = val[2];
      if (this.mget('inner_only') && !this.plot_view.frame.contains(vx, vy)) {
        continue;
      }
      tip = $('<div />').appendTo(this.$el);
      tip.append(content);
    }
    sx = this.plot_view.mget('canvas').vx_to_sx(vx);
    sy = this.plot_view.mget('canvas').vy_to_sy(vy);
    side = this.mget('side');
    if (side === 'auto') {
      ow = this.plot_view.frame.get('width');
      if (vx - this.plot_view.frame.get('left') < ow / 2) {
        side = 'right';
      } else {
        side = 'left';
      }
    }
    this.$el.removeClass('bk-right');
    this.$el.removeClass('bk-left');
    arrow_width = 10;
    switch (side) {
      case "right":
        this.$el.addClass("bk-left");
        left = sx + (this.$el.outerWidth() - this.$el.innerWidth()) + arrow_width;
        break;
      case "left":
        this.$el.addClass("bk-right");
        left = sx - this.$el.outerWidth() - arrow_width;
    }
    top = sy - this.$el.outerHeight() / 2;
    if (this.$el.children().length > 0) {
      this.$el.css({
        top: top,
        left: left
      });
      return this.$el.show();
    }
  };

  return TooltipView;

})(PlotWidget);

Tooltip = (function(superClass) {
  extend(Tooltip, superClass);

  function Tooltip() {
    return Tooltip.__super__.constructor.apply(this, arguments);
  }

  Tooltip.prototype.default_view = TooltipView;

  Tooltip.prototype.type = 'Tooltip';

  Tooltip.prototype.nonserializable_attribute_names = function() {
    return Tooltip.__super__.nonserializable_attribute_names.call(this).concat(['data', 'custom']);
  };

  Tooltip.prototype.clear = function() {
    return this.set('data', []);
  };

  Tooltip.prototype.add = function(vx, vy, content) {
    var data;
    data = this.get('data');
    data.push([vx, vy, content]);
    return this.set('data', data);
  };

  Tooltip.prototype.defaults = function() {
    return _.extend({}, Tooltip.__super__.defaults.call(this), {
      level: 'overlay',
      side: "auto",
      inner_only: true
    });
  };

  return Tooltip;

})(Annotation.Model);

module.exports = {
  Model: Tooltip,
  View: TooltipView
};
