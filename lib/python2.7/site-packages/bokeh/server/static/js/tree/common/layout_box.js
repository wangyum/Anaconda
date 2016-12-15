var Constraint, Eq, Expression, Ge, LayoutBox, Le, Model, Operator, Range1d, Variable, _, kiwi,
  extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty;

_ = require("underscore");

kiwi = require("kiwi");

Variable = kiwi.Variable, Expression = kiwi.Expression, Constraint = kiwi.Constraint, Operator = kiwi.Operator;

Eq = Operator.Eq, Le = Operator.Le, Ge = Operator.Ge;

Model = require("../model");

Range1d = require("../models/ranges/range1d");

LayoutBox = (function(superClass) {
  extend(LayoutBox, superClass);

  LayoutBox.prototype.type = 'LayoutBox';

  LayoutBox.prototype.nonserializable_attribute_names = function() {
    return LayoutBox.__super__.nonserializable_attribute_names.call(this).concat(['solver', 'layout_location']);
  };

  function LayoutBox(attrs, options) {
    this.solver = null;
    this._initialized = false;
    LayoutBox.__super__.constructor.call(this, attrs, options);
  }

  LayoutBox.prototype.initialize = function(attrs, options) {
    LayoutBox.__super__.initialize.call(this, attrs, options);
    this._initialized = true;
    return this._initialize_if_we_have_solver();
  };

  LayoutBox.prototype.set = function(key, value, options) {
    LayoutBox.__super__.set.call(this, key, value, options);
    return this._initialize_if_we_have_solver();
  };

  LayoutBox.prototype._initialize_if_we_have_solver = function() {
    var i, j, len, len1, name, ref, ref1, v;
    if (!this._initialized) {
      return;
    }
    if (this.solver != null) {
      if (this.get('solver') !== this.solver) {
        throw new Error("We do not support changing the solver attribute on LayoutBox");
      }
      return;
    }
    this.solver = this.get('solver');
    if (this.solver == null) {
      return;
    }
    this.var_constraints = {};
    ref = ['top', 'left', 'width', 'height'];
    for (i = 0, len = ref.length; i < len; i++) {
      v = ref[i];
      name = '_' + v;
      this[name] = new Variable(v);
      this.register_property(v, this._get_var, false);
      this.register_setter(v, this._set_var);
      this.solver.add_edit_variable(this[name], kiwi.Strength.strong);
    }
    ref1 = ['right', 'bottom'];
    for (j = 0, len1 = ref1.length; j < len1; j++) {
      v = ref1[j];
      name = '_' + v;
      this[name] = new Variable(v);
      this.register_property(v, this._get_var, false);
    }
    this.solver.add_constraint(new Constraint(new Expression(this._top), Ge));
    this.solver.add_constraint(new Constraint(new Expression(this._bottom), Ge));
    this.solver.add_constraint(new Constraint(new Expression(this._left), Ge));
    this.solver.add_constraint(new Constraint(new Expression(this._right), Ge));
    this.solver.add_constraint(new Constraint(new Expression(this._width), Ge));
    this.solver.add_constraint(new Constraint(new Expression(this._height), Ge));
    this.solver.add_constraint(new Constraint(new Expression(this._left, this._width, [-1, this._right]), Eq));
    this.solver.add_constraint(new Constraint(new Expression(this._bottom, this._height, [-1, this._top]), Eq));
    this._h_range = new Range1d.Model({
      start: this.get('left'),
      end: this.get('left') + this.get('width')
    });
    this.register_property('h_range', (function(_this) {
      return function() {
        _this._h_range.set('start', _this.get('left'));
        _this._h_range.set('end', _this.get('left') + _this.get('width'));
        return _this._h_range;
      };
    })(this), false);
    this.add_dependencies('h_range', this, ['left', 'width']);
    this._v_range = new Range1d.Model({
      start: this.get('bottom'),
      end: this.get('bottom') + this.get('height')
    });
    this.register_property('v_range', (function(_this) {
      return function() {
        _this._v_range.set('start', _this.get('bottom'));
        _this._v_range.set('end', _this.get('bottom') + _this.get('height'));
        return _this._v_range;
      };
    })(this), false);
    this.add_dependencies('v_range', this, ['bottom', 'height']);
    this._aspect_constraint = null;
    this.register_property('aspect', (function(_this) {
      return function() {
        return _this.get('width') / _this.get('height');
      };
    })(this), true);
    this.register_setter('aspect', this._set_aspect);
    return this.add_dependencies('aspect', this, ['width', 'height']);
  };

  LayoutBox.prototype.contains = function(vx, vy) {
    return vx >= this.get('left') && vx <= this.get('right') && vy >= this.get('bottom') && vy <= this.get('top');
  };

  LayoutBox.prototype._set_var = function(value, prop_name) {
    var c, v;
    v = this['_' + prop_name];
    if (_.isNumber(value)) {
      return this.solver.suggest_value(v, value);
    } else if (_.isString(value)) {

    } else {
      c = new Constraint(new Expression(v, [-1, value]), Eq);
      if (this.var_constraints[prop_name] == null) {
        this.var_constraints[prop_name] = [];
      }
      this.var_constraints[prop_name].push(c);
      return this.solver.add_constraint(c);
    }
  };

  LayoutBox.prototype._get_var = function(prop_name) {
    return this['_' + prop_name].value();
  };

  LayoutBox.prototype._set_aspect = function(aspect) {
    var c;
    if (this._aspect_constraint != null) {
      this.solver.remove_constraint(this.aspect_constraint);
      c = new Constraint(new Expression([aspect, this._height], [-1, this._width]), Eq);
      this._aspect_constraint = c;
      return this.solver.add_constraint(c);
    }
  };

  return LayoutBox;

})(Model);

module.exports = {
  Model: LayoutBox
};
