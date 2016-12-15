var $2, ContinuumView, InputWidget, Slider, SliderView, _, logger, slidertemplate,
  bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; },
  extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty;

_ = require("underscore");

$2 = require("jquery-ui/slider");

ContinuumView = require("../../common/continuum_view");

logger = require("../../common/logging").logger;

slidertemplate = require("./slidertemplate");

InputWidget = require("./input_widget");

SliderView = (function(superClass) {
  extend(SliderView, superClass);

  function SliderView() {
    this.slide = bind(this.slide, this);
    return SliderView.__super__.constructor.apply(this, arguments);
  }

  SliderView.prototype.tagName = "div";

  SliderView.prototype.template = slidertemplate;

  SliderView.prototype.initialize = function(options) {
    var html;
    SliderView.__super__.initialize.call(this, options);
    this.listenTo(this.model, 'change', this.render);
    this.$el.empty();
    html = this.template(this.model.attributes);
    this.$el.html(html);
    return this.render();
  };

  SliderView.prototype.render = function() {
    var max, min, step;
    max = this.mget('end');
    min = this.mget('start');
    step = this.mget('step') || ((max - min) / 50);
    logger.debug("slider render: min, max, step = (" + min + ", " + max + ", " + step + ")");
    this.$('.slider').slider({
      orientation: this.mget('orientation'),
      animate: "fast",
      slide: _.throttle(this.slide, 200),
      value: this.mget('value'),
      min: min,
      max: max,
      step: step
    });
    this.$("#" + (this.mget('id'))).val(this.$('.slider').slider('value'));
    return this;
  };

  SliderView.prototype.slide = function(event, ui) {
    var ref, value;
    value = ui.value;
    logger.debug("slide value = " + value);
    this.$("#" + (this.mget('id'))).val(ui.value);
    this.mset('value', value);
    return (ref = this.mget('callback')) != null ? ref.execute(this.model) : void 0;
  };

  return SliderView;

})(ContinuumView);

Slider = (function(superClass) {
  extend(Slider, superClass);

  function Slider() {
    return Slider.__super__.constructor.apply(this, arguments);
  }

  Slider.prototype.type = "Slider";

  Slider.prototype.default_view = SliderView;

  Slider.prototype.defaults = function() {
    return _.extend({}, Slider.__super__.defaults.call(this), {
      title: '',
      value: 0.5,
      start: 0,
      end: 1,
      step: 0.1,
      orientation: "horizontal"
    });
  };

  return Slider;

})(InputWidget.Model);

module.exports = {
  Model: Slider,
  View: SliderView
};
