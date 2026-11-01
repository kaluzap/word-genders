class SuccessStreak:
    def __init__(self):
        # list of succes streaks
        self.success_streak_history = []
        # actual success streak
        self.success_streak = 0
        # success streak record
        self.success_streak_record = 0
        # is record
        self.is_record = False

    def add_new_sucess(self):
        self.success_streak += 1
        if self.success_streak > self.success_streak_record:
            self.is_record = True
            self.success_streak_record = self.success_streak
        else:
            self.is_record = False

    def stop_success_streak(self):
        self.success_streak_history.append(self.success_streak)
        self.success_streak = 0
        self.success_streak_record = max(self.success_streak_history)
