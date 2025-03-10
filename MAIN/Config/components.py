class ALU:
    def ADD(self, dest, src1, src2):
        proc.setreg(dest, proc.getreg(src1) + proc.getreg(src2))
    def SUB(self, dest, src1, src2):
        proc.setreg(dest, proc.getreg(src1) - proc.getreg(src2))
    # etc