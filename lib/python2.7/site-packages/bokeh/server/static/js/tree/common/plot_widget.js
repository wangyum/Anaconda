var ContinuumView, PlotWidget,
  extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty;

ContinuumView = require("./continuum_view");

PlotWidget = (function(superClass) {
  extend(PlotWidget, superClass);

  function PlotWidget() {
    return PlotWidget.__super__.constructor.apply(this, arguments);
  }

  PlotWidget.prototype.tagName = 'div';

  PlotWidget.prototype.initialize = function(options) {
    this.plot_model = options.plot_model;
    return this.plot_view = options.plot_view;
  };

  PlotWidget.prototype.bind_bokeh_events = function() {};

  PlotWidget.prototype.request_render = function() {
    return this.plot_view.request_render();
  };

  module.exports = PlotWidget;

  return PlotWidget;

})(ContinuumView);
