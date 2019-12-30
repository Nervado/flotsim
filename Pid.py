# implements a discret PID by @nervado


class Pid:

    def __init__(self, P=2.0, I=0.0, D=0.0, maxO=100, minO=0):

        self.Kp = P
        self.Ki = I
        self.Kd = D

        self.max = maxO
        self.min = minO

        self.set_point = 0.0
        self.error = 0.0

        self.derivative = 0
        self.integral = 0

        self.previus_error = 0

        self.previous_out = 0

    def update(self, measured_value, dt):

        self.error = self.set_point - measured_value
        self.integral = self.integral + self.error * dt
        self.derivative = (self.error - self.previus_error)/dt
        self.previus_error = self.error

        pid_out = self.Kp * self.error + self.Ki * \
            self.integral + self.Kd * self.derivative + self.previous_out

        # ant-reset windup

        if pid_out > self.max:
            pid_out = self.max
            self.integral = 0

        if pid_out < self.min:
            pid_out = self.min
            self.integral = 0

        self.previus_error = self.error
        self.previous_out = pid_out

        return pid_out

    def setPoint(self, set_point):

        self.set_point = set_point
        self.integral = 0
