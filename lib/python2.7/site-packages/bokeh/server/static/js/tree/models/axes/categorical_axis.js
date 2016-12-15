var Axis, CategoricalAxis, CategoricalAxisView, CategoricalTickFormatter, CategoricalTicker, _, logger,
  extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty;

_ = require("underscore");

logger = require("../../common/logging").logger;

CategoricalTicker = require("../tickers/categorical_ticker");

CategoricalTickFormatter = require("../formatters/categorical_tick_formatter");

Axis = require("./axis");

CategoricalAxisView = (function(superClass) {
  extend(CategoricalAxisView, superClass);

  function CategoricalAxisView() {
    return CategoricalAxisView.__super__.constructor.apply(this, arguments);
  }

  return CategoricalAxisView;

})(Axis.View);

CategoricalAxis = (function(superClass) {
  extend(CategoricalAxis, superClass);

  function CategoricalAxis() {
    return CategoricalAxis.__super__.constructor.apply(this, arguments);
  }

  CategoricalAxis.prototype.default_view = CategoricalAxisView;

  CategoricalAxis.prototype.type = 'CategoricalAxis';

  CategoricalAxis.prototype.defaults = function() {
    return _.extend({}, CategoricalAxis.__super__.defaults.call(this), {
      ticker: new CategoricalTicker.Model(),
      formatter: new CategoricalTickFormatter.Model()
    });
  };

  CategoricalAxis.prototype._computed_bounds = function() {
    var cross_range, range, range_bounds, ref, ref1, user_bounds;
    ref = this.get('ranges'), range = ref[0], cross_range = ref[1];
    user_bounds = (ref1 = this.get('bounds')) != null ? ref1 : 'auto';
    range_bounds = [range.get('min'), range.get('max')];
    if (user_bounds !== 'auto') {
      logger.warn("Categorical Axes only support user_bounds='auto', ignoring");
    }
    return range_bounds;
  };

  return CategoricalAxis;

})(Axis.Model);

module.exports = {
  Model: CategoricalAxis,
  View: CategoricalAxisView
};
