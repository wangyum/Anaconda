var ContinuousTicker, FixedTicker, _,
  extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty;

_ = require("underscore");

ContinuousTicker = require("./continuous_ticker");

FixedTicker = (function(superClass) {
  extend(FixedTicker, superClass);

  function FixedTicker() {
    return FixedTicker.__super__.constructor.apply(this, arguments);
  }

  FixedTicker.prototype.type = 'FixedTicker';

  FixedTicker.prototype.get_ticks_no_defaults = function(data_low, data_high, desired_n_ticks) {
    return {
      major: this.get('ticks'),
      minor: []
    };
  };

  FixedTicker.prototype.defaults = function() {
    return _.extend({}, FixedTicker.__super__.defaults.call(this), {
      ticks: []
    });
  };

  return FixedTicker;

})(ContinuousTicker.Model);

module.exports = {
  Model: FixedTicker
};
