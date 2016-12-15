var Axis, BasicTickFormatter, BasicTicker, ContinuousAxis, LinearAxis, LinearAxisView, _,
  extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty;

_ = require("underscore");

Axis = require("./axis");

ContinuousAxis = require("./continuous_axis");

BasicTicker = require("../tickers/basic_ticker");

BasicTickFormatter = require("../formatters/basic_tick_formatter");

LinearAxisView = (function(superClass) {
  extend(LinearAxisView, superClass);

  function LinearAxisView() {
    return LinearAxisView.__super__.constructor.apply(this, arguments);
  }

  return LinearAxisView;

})(Axis.View);

LinearAxis = (function(superClass) {
  extend(LinearAxis, superClass);

  function LinearAxis() {
    return LinearAxis.__super__.constructor.apply(this, arguments);
  }

  LinearAxis.prototype.default_view = LinearAxisView;

  LinearAxis.prototype.type = 'LinearAxis';

  LinearAxis.prototype.defaults = function() {
    return _.extend({}, LinearAxis.__super__.defaults.call(this), {
      ticker: new BasicTicker.Model(),
      formatter: new BasicTickFormatter.Model()
    });
  };

  return LinearAxis;

})(ContinuousAxis.Model);

module.exports = {
  Model: LinearAxis,
  View: LinearAxisView
};
