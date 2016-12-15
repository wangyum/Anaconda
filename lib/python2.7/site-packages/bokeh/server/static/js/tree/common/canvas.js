var Canvas, CanvasView, Constraint, ContinuumView, Expression, LayoutBox, Operator, Solver, _, canvas_template, kiwi, logger,
  extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty;

_ = require("underscore");

kiwi = require("kiwi");

Expression = kiwi.Expression, Constraint = kiwi.Constraint, Operator = kiwi.Operator;

canvas_template = require("./canvas_template");

ContinuumView = require("./continuum_view");

LayoutBox = require("./layout_box");

logger = require("./logging").logger;

Solver = require("./solver");

CanvasView = (function(superClass) {
  extend(CanvasView, superClass);

  function CanvasView() {
    return CanvasView.__super__.constructor.apply(this, arguments);
  }

  CanvasView.prototype.className = "bk-canvas-wrapper";

  CanvasView.prototype.template = canvas_template;

  CanvasView.prototype.initialize = function(options) {
    var html, ref, template_data;
    CanvasView.__super__.initialize.call(this, options);
    template_data = {
      map: this.mget('map')
    };
    html = this.template(template_data);
    this.$el.html(html);
    this.canvas_wrapper = this.$el;
    this.canvas = this.$('canvas.bk-canvas');
    this.canvas_events = this.$('div.bk-canvas-events');
    this.canvas_overlay = this.$('div.bk-canvas-overlays');
    this.map_div = (ref = this.$('div.bk-canvas-map')) != null ? ref : null;
    this.ctx = this.canvas[0].getContext('2d');
    this.ctx.glcanvas = null;
    return logger.debug("CanvasView initialized");
  };

  CanvasView.prototype.render = function(force) {
    var backingStoreRatio, devicePixelRatio, height, ratio, width;
    if (force == null) {
      force = false;
    }
    if (!this.model.new_bounds && !force) {
      return;
    }
    if (this.mget('use_hidpi')) {
      devicePixelRatio = window.devicePixelRatio || 1;
      backingStoreRatio = this.ctx.webkitBackingStorePixelRatio || this.ctx.mozBackingStorePixelRatio || this.ctx.msBackingStorePixelRatio || this.ctx.oBackingStorePixelRatio || this.ctx.backingStorePixelRatio || 1;
      ratio = devicePixelRatio / backingStoreRatio;
    } else {
      ratio = 1;
    }
    width = this.mget('width');
    height = this.mget('height');
    this.$el.attr('style', "z-index: 50; width:" + width + "px; height:" + height + "px");
    this.canvas.attr('style', "width:" + width + "px;height:" + height + "px");
    this.canvas.attr('width', width * ratio).attr('height', height * ratio);
    this.$el.attr("width", width).attr('height', height);
    this.canvas_events.attr('style', "z-index:100; position:absolute; top:0; left:0; width:" + width + "px; height:" + height + "px;");
    this.canvas_overlay.attr('style', "z-index:75; position:absolute; top:0; left:0; width:" + width + "px; height:" + height + "px;");
    this.ctx.scale(ratio, ratio);
    this.ctx.translate(0.5, 0.5);
    this._fixup_line_dash(this.ctx);
    this._fixup_line_dash_offset(this.ctx);
    this._fixup_image_smoothing(this.ctx);
    this._fixup_measure_text(this.ctx);
    return this.model.new_bounds = false;
  };

  CanvasView.prototype._fixup_line_dash = function(ctx) {
    if (!ctx.setLineDash) {
      ctx.setLineDash = function(dash) {
        ctx.mozDash = dash;
        return ctx.webkitLineDash = dash;
      };
    }
    if (!ctx.getLineDash) {
      return ctx.getLineDash = function() {
        return ctx.mozDash;
      };
    }
  };

  CanvasView.prototype._fixup_line_dash_offset = function(ctx) {
    ctx.setLineDashOffset = function(dash_offset) {
      ctx.lineDashOffset = dash_offset;
      ctx.mozDashOffset = dash_offset;
      return ctx.webkitLineDashOffset = dash_offset;
    };
    return ctx.getLineDashOffset = function() {
      return ctx.mozDashOffset;
    };
  };

  CanvasView.prototype._fixup_image_smoothing = function(ctx) {
    ctx.setImageSmoothingEnabled = function(value) {
      ctx.imageSmoothingEnabled = value;
      ctx.mozImageSmoothingEnabled = value;
      ctx.oImageSmoothingEnabled = value;
      return ctx.webkitImageSmoothingEnabled = value;
    };
    return ctx.getImageSmoothingEnabled = function() {
      var ref;
      return (ref = ctx.imageSmoothingEnabled) != null ? ref : true;
    };
  };

  CanvasView.prototype._fixup_measure_text = function(ctx) {
    if (ctx.measureText && (ctx.html5MeasureText == null)) {
      ctx.html5MeasureText = ctx.measureText;
      return ctx.measureText = function(text) {
        var textMetrics;
        textMetrics = ctx.html5MeasureText(text);
        textMetrics.ascent = ctx.html5MeasureText("m").width * 1.6;
        return textMetrics;
      };
    }
  };

  return CanvasView;

})(ContinuumView);

Canvas = (function(superClass) {
  extend(Canvas, superClass);

  function Canvas() {
    return Canvas.__super__.constructor.apply(this, arguments);
  }

  Canvas.prototype.type = 'Canvas';

  Canvas.prototype.default_view = CanvasView;

  Canvas.prototype.initialize = function(attr, options) {
    var solver;
    solver = new Solver();
    this.set('solver', solver);
    Canvas.__super__.initialize.call(this, attr, options);
    this.new_bounds = true;
    solver.add_constraint(new Constraint(new Expression(this._left), Operator.Eq));
    solver.add_constraint(new Constraint(new Expression(this._bottom), Operator.Eq));
    this._set_dims([this.get('canvas_width'), this.get('canvas_height')]);
    return logger.debug("Canvas initialized");
  };

  Canvas.prototype.vx_to_sx = function(x) {
    return x;
  };

  Canvas.prototype.vy_to_sy = function(y) {
    return this.get('height') - (y + 1);
  };

  Canvas.prototype.v_vx_to_sx = function(xx) {
    var i, idx, len, x;
    for (idx = i = 0, len = xx.length; i < len; idx = ++i) {
      x = xx[idx];
      xx[idx] = x;
    }
    return xx;
  };

  Canvas.prototype.v_vy_to_sy = function(yy) {
    var canvas_height, i, idx, len, y;
    canvas_height = this.get('height');
    for (idx = i = 0, len = yy.length; i < len; idx = ++i) {
      y = yy[idx];
      yy[idx] = canvas_height - (y + 1);
    }
    return yy;
  };

  Canvas.prototype.sx_to_vx = function(x) {
    return x;
  };

  Canvas.prototype.sy_to_vy = function(y) {
    return this.get('height') - (y + 1);
  };

  Canvas.prototype.v_sx_to_vx = function(xx) {
    var i, idx, len, x;
    for (idx = i = 0, len = xx.length; i < len; idx = ++i) {
      x = xx[idx];
      xx[idx] = x;
    }
    return xx;
  };

  Canvas.prototype.v_sy_to_vy = function(yy) {
    var canvas_height, i, idx, len, y;
    canvas_height = this.get('height');
    for (idx = i = 0, len = yy.length; i < len; idx = ++i) {
      y = yy[idx];
      yy[idx] = canvas_height - (y + 1);
    }
    return yy;
  };

  Canvas.prototype._set_width = function(width, update) {
    if (update == null) {
      update = true;
    }
    if (this._width_constraint != null) {
      this.solver.remove_constraint(this._width_constraint);
    }
    this._width_constraint = new Constraint(new Expression(this._width, -width), Operator.Eq);
    this.solver.add_constraint(this._width_constraint);
    if (update) {
      this.solver.update_variables();
    }
    return this.new_bounds = true;
  };

  Canvas.prototype._set_height = function(height, update) {
    if (update == null) {
      update = true;
    }
    if (this._height_constraint != null) {
      this.solver.remove_constraint(this._height_constraint);
    }
    this._height_constraint = new Constraint(new Expression(this._height, -height), Operator.Eq);
    this.solver.add_constraint(this._height_constraint);
    if (update) {
      this.solver.update_variables();
    }
    return this.new_bounds = true;
  };

  Canvas.prototype._set_dims = function(dims, trigger) {
    if (trigger == null) {
      trigger = true;
    }
    this._set_width(dims[0], false);
    this._set_height(dims[1], false);
    return this.solver.update_variables(trigger);
  };

  Canvas.prototype.defaults = function() {
    return _.extend({}, Canvas.__super__.defaults.call(this), {
      width: 300,
      height: 300,
      map: false,
      mousedown_callbacks: [],
      mousemove_callbacks: [],
      use_hidpi: true
    });
  };

  return Canvas;

})(LayoutBox.Model);

module.exports = {
  Model: Canvas
};
