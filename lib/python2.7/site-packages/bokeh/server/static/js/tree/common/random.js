var Random;

Random = (function() {
  function Random(seed1) {
    var ref;
    this.seed = seed1;
    this.multiplier = 1664525;
    this.modulo = 4294967296;
    this.offset = 1013904223;
    if (!((this.seed != null) && (0 <= (ref = this.seed) && ref < this.modulo))) {
      this.seed = (new Date().valueOf() * new Date().getMilliseconds()) % this.modulo;
    }
  }

  Random.prototype.seed = function(seed) {
    return this.seed = seed;
  };

  Random.prototype.randn = function() {
    return this.seed = (this.multiplier * this.seed + this.offset) % this.modulo;
  };

  Random.prototype.randf = function() {
    return this.randn() / this.modulo;
  };

  Random.prototype.rand = function(n) {
    return Math.floor(this.randf() * n);
  };

  Random.prototype.rand2 = function(min, max) {
    return min + this.rand(max - min);
  };

  return Random;

})();

module.exports = Random;
