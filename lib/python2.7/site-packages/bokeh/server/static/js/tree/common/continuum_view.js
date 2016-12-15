var Backbone, ContinuumView, _,
  extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty;

_ = require("underscore");

Backbone = require("backbone");

ContinuumView = (function(superClass) {
  extend(ContinuumView, superClass);

  function ContinuumView() {
    return ContinuumView.__super__.constructor.apply(this, arguments);
  }

  ContinuumView.prototype.initialize = function(options) {
    if (!_.has(options, 'id')) {
      return this.id = _.uniqueId('ContinuumView');
    }
  };

  ContinuumView.prototype.bind_bokeh_events = function() {
    return 'pass';
  };

  ContinuumView.prototype.delegateEvents = function(events) {
    return ContinuumView.__super__.delegateEvents.call(this, events);
  };

  ContinuumView.prototype.remove = function() {
    var ref, target, val;
    if (_.has(this, 'eventers')) {
      ref = this.eventers;
      for (target in ref) {
        if (!hasProp.call(ref, target)) continue;
        val = ref[target];
        val.off(null, null, this);
      }
    }
    this.trigger('remove', this);
    return ContinuumView.__super__.remove.call(this);
  };

  ContinuumView.prototype.mget = function() {
    return this.model.get.apply(this.model, arguments);
  };

  ContinuumView.prototype.mset = function() {
    return this.model.set.apply(this.model, arguments);
  };

  ContinuumView.prototype.render_end = function() {
    return "pass";
  };

  return ContinuumView;

})(Backbone.View);

module.exports = ContinuumView;
