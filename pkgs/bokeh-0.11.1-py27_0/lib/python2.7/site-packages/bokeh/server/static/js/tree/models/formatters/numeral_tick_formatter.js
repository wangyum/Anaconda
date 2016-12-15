var Numeral, NumeralTickFormatter, TickFormatter, _,
  extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty;

_ = require("underscore");

Numeral = require("numeral");

TickFormatter = require("./tick_formatter");

NumeralTickFormatter = (function(superClass) {
  extend(NumeralTickFormatter, superClass);

  function NumeralTickFormatter() {
    return NumeralTickFormatter.__super__.constructor.apply(this, arguments);
  }

  NumeralTickFormatter.prototype.type = 'NumeralTickFormatter';

  NumeralTickFormatter.prototype.format = function(ticks) {
    var format, labels, language, rounding, tick;
    format = this.get("format");
    language = this.get("language");
    rounding = (function() {
      switch (this.get("rounding")) {
        case "round":
        case "nearest":
          return Math.round;
        case "floor":
        case "rounddown":
          return Math.floor;
        case "ceil":
        case "roundup":
          return Math.ceil;
      }
    }).call(this);
    labels = (function() {
      var i, len, results;
      results = [];
      for (i = 0, len = ticks.length; i < len; i++) {
        tick = ticks[i];
        results.push(Numeral.format(tick, format, language, rounding));
      }
      return results;
    })();
    return labels;
  };

  NumeralTickFormatter.prototype.defaults = function() {
    return _.extend({}, NumeralTickFormatter.__super__.defaults.call(this), {
      format: '0,0',
      language: 'en',
      rounding: 'round'
    });
  };

  return NumeralTickFormatter;

})(TickFormatter.Model);

module.exports = {
  Model: NumeralTickFormatter
};
