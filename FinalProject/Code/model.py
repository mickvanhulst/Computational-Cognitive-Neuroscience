from chainer import Chain
from chainer import reporter


class Model(Chain):
	"""
	General implementation of a Model class
	"""

	compute_accuracy = False

	def __init__(self, predictor, lossfun, accfun):
		"""
		:param predictor: Chain that predicts output given input; the network
		:param lossfun: loss function
		:param accfun: accuracy function
		"""
		super(Model, self).__init__()
		with self.init_scope():
			self.lossfun = lossfun
			self.accfun = accfun
			self.y = None
			self.loss = None
			self.accuracy = None
			self.predictor = predictor

	def __call__(self, x, t):
		self.y = None
		self.loss = None
		self.accuracy = None
		self.y = self.predictor(x)
		self.loss = self.lossfun(self.y, t)
		reporter.report({'loss': self.loss}, self)
		if self.compute_accuracy:
			self.accuracy = self.accfun(self.y, t)
			reporter.report({'accuracy': self.accuracy}, self)
		return self.loss

	def predict(self, x):
		self.y = self.predictor(x)

		return self.y
