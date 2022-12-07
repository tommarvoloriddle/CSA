import os
import argparse

MemSize = 1000 # memory size, in reality, the memory size should be 2^32, but for this lab, for the space resaon, we keep it as this large number, but the memory is still 32-bit addressable.

class InsMem(object):
    def __init__(self, name, ioDir):
        self.id = name
        self.instructions = []
        with open(ioDir + "\\imem.txt") as im:
            self.IMem = [data.replace("\n", "") for data in im.readlines()]
        # print(self.IMem)

        self.table = {}
        self.RISCV_table = {}
        self.fill_RISCV()
        self.readInstr(self.IMem)

    def fill_RISCV(self):
        # fill the data memory
        # return the data memory
        self.RISCV_table = {
            'opcode': { 
                '0110011' : 'R',
                '0010011' : 'I',
                '1101111' : 'J',
                '1100011' : 'SB',
                '0000011' : 'LW',
                '0100011' : 'S',
                '1111111' : 'HALT',
            },
            'instr': { 
                'ADD' : '0110011',
                'SUB' : '0110011',
                'XOR' : '0110011',
                'OR'  : '0110011',
                'AND' : '0110011',
                'ADDI': '0010011',
                'XORI': '0010011',
                'ORI' : '0010011',
                'ANDI': '0010011',
                'JAL': '1101111',
                'BEQ': '1100011',
                'BNE': '1100011',
                'LW':  '0000011',
                'SW':  '0100011',
                'HALT': '1111111',
            },
        }

    def fill_opcodes(self):
        # fill the opcode table
        # return the opcode table
        for instruction in self.instructions:
            self.table[instruction] = {
                'opcode': instruction[25:32],
                'instr_type': self.RISCV_table['opcode'][instruction[25:32]],
                'instr_name': None,
            }

    def fill_destionation_register(self):
        # fill the destination register
        # return the destination register
        for instruction in self.instructions:
            if self.table[instruction]['instr_type'] == 'R':
                self.table[instruction]['dest_reg'] = instruction[20:25]
            elif self.table[instruction]['instr_type'] == 'I':
                self.table[instruction]['dest_reg'] = instruction[20:25]
            elif self.table[instruction]['instr_type'] == 'J':
                self.table[instruction]['dest_reg'] = instruction[20:25]
            elif self.table[instruction]['instr_type'] == 'LW':
                self.table[instruction]['dest_reg'] = instruction[20:25]
            elif self.table[instruction]['instr_type'] == 'HALT':
                self.table[instruction]['dest_reg'] = None
            elif self.table[instruction]['instr_type'] == 'S':
                self.table[instruction]['dest_reg'] = None
            elif self.table[instruction]['instr_type'] == 'SB':
                self.table[instruction]['dest_reg'] = None

    def fill_source_register(self):
        # fill the source register
        # return the source register
        for instruction in self.instructions:
            if self.table[instruction]['instr_type'] == 'R':
                self.table[instruction]['src_reg1'] = instruction[12:17]
                self.table[instruction]['src_reg2'] = instruction[7:12]
            elif self.table[instruction]['instr_type'] == 'I':
                self.table[instruction]['src_reg1'] = instruction[12:17]
                self.table[instruction]['src_reg2'] = None
            elif self.table[instruction]['instr_type'] == 'J':
                self.table[instruction]['src_reg1'] = None
                self.table[instruction]['src_reg2'] = None
            elif self.table[instruction]['instr_type'] == 'LW':
                self.table[instruction]['src_reg1'] = instruction[12:17]
                self.table[instruction]['src_reg2'] = None
            elif self.table[instruction]['instr_type'] == 'HALT':
                self.table[instruction]['src_reg1'] = None
                self.table[instruction]['src_reg2'] = None
            elif self.table[instruction]['instr_type'] == 'SB':
                self.table[instruction]['src_reg1'] = instruction[12:17]
                self.table[instruction]['src_reg2'] = instruction[7:12]
            elif self.table[instruction]['instr_type'] == 'S':
                self.table[instruction]['src_reg1'] = instruction[12:17]
                self.table[instruction]['src_reg2'] = instruction[7:12]

    def fill_function3(self):
        # fill the function3
        # return the function3
        for instruction in self.instructions:
            if self.table[instruction]['instr_type'] == 'R':
                self.table[instruction]['func3'] = instruction[17:20]
            elif self.table[instruction]['instr_type'] == 'I':
                self.table[instruction]['func3'] = instruction[17:20]
            elif self.table[instruction]['instr_type'] == 'SB':
                self.table[instruction]['func3'] = instruction[17:20]
            elif self.table[instruction]['instr_type'] == 'S':
                self.table[instruction]['func3'] = instruction[17:20]
            elif self.table[instruction]['instr_type'] == 'LW':
                self.table[instruction]['func3'] = instruction[17:20]
            elif self.table[instruction]['instr_type'] == 'HALT':
                self.table[instruction]['func3'] = None
            
    def fill_function7(self):
        # fill the function7
        # return the function7
        for instruction in self.instructions:
            if self.table[instruction]['instr_type'] == 'R':
                self.table[instruction]['func7'] = instruction[0:7]
            elif self.table[instruction]['instr_type'] == 'HALT':
                self.table[instruction]['func7'] = None
    
    def fill_immediate(self):
        # fill the immediate
        # return the immediate
        for instruction in self.instructions:
            if self.table[instruction]['instr_type'] == 'I':
                self.table[instruction]['imm'] = instruction[0:12]
            elif self.table[instruction]['instr_type'] == 'SB':
                self.table[instruction]['imm'] = instruction[0] + instruction[24] + instruction[1:6] + instruction[20:24]
            elif self.table[instruction]['instr_type'] == 'LW':
                self.table[instruction]['imm'] = instruction[0:12]
            elif self.table[instruction]['instr_type'] == 'J':
                self.table[instruction]['imm'] = instruction[0] + instruction[13:20] + instruction[12] + instruction[1:12]
            elif self.table[instruction]['instr_type'] == 'HALT':
                self.table[instruction]['imm'] = None
            elif self.table[instruction]['instr_type'] == 'S':
                self.table[instruction]['imm'] = instruction[0:7] + instruction[20:25]

    def fill_instr_name(self):
        # fill the instruction name
        # return the instruction name
        for instruction in self.instructions:
            # print(self.table[instruction]['instr_type'])
            if self.table[instruction]['instr_type'] == 'R':
                if self.table[instruction]['func3'] == '000':
                    if self.table[instruction]['func7'] == '0000000':
                        self.table[instruction]['instr_name'] = 'ADD'
                    elif self.table[instruction]['func7'] == '0100000':
                        self.table[instruction]['instr_name'] = 'SUB'
                elif self.table[instruction]['func3'] == '001':
                    self.table[instruction]['instr_name'] = 'SLL'
                elif self.table[instruction]['func3'] == '010':
                    self.table[instruction]['instr_name'] = 'SLT'
                elif self.table[instruction]['func3'] == '011':
                    self.table[instruction]['instr_name'] = 'SLTU'
                elif self.table[instruction]['func3'] == '100':
                    self.table[instruction]['instr_name'] = 'XOR'
                elif self.table[instruction]['func3'] == '101':
                    if self.table[instruction]['func7'] == '0000000':
                        self.table[instruction]['instr_name'] = 'SRL'
                    elif self.table[instruction]['func7'] == '0100000':
                        self.table[instruction]['instr_name'] = 'SRA'
                elif self.table[instruction]['func3'] == '110':
                    self.table[instruction]['instr_name'] = 'OR'
                elif self.table[instruction]['func3'] == '111':
                    self.table[instruction]['instr_name'] = 'AND'
            elif self.table[instruction]['instr_type'] == 'I':
                if self.table[instruction]['func3'] == '000':
                    self.table[instruction]['instr_name'] = 'ADDI'
                elif self.table[instruction]['func3'] == '001':
                    self.table[instruction]['instr_name'] = 'SLLI'
                elif self.table[instruction]['func3'] == '010':
                    self.table[instruction]['instr_name'] = 'SLTI'
                elif self.table[instruction]['func3'] == '011':
                    self.table[instruction]['instr_name'] = 'SLTIU'
                elif self.table[instruction]['func3'] == '100':
                    self.table[instruction]['instr_name'] = 'XORI'
                elif self.table[instruction]['func3'] == '101':
                    self.table[instruction]['instr_name'] = 'SRLI'
                elif self.table[instruction]['func3'] == '110':
                    self.table[instruction]['instr_name'] = 'ORI'
                elif self.table[instruction]['func3'] == '111':
                    self.table[instruction]['instr_name'] = 'ANDI'
            elif self.table[instruction]['instr_type'] == 'SB':
                if self.table[instruction]['func3'] == '000':
                    self.table[instruction]['instr_name'] = 'BEQ'
                elif self.table[instruction]['func3'] == '001':
                    self.table[instruction]['instr_name'] = 'BNE'
                elif self.table[instruction]['func3'] == '100':
                    self.table[instruction]['instr_name'] = 'BLT'
                elif self.table[instruction]['func3'] == '101':
                    self.table[instruction]['instr_name'] = 'BGE'
                elif self.table[instruction]['func3'] == '110':
                    self.table[instruction]['instr_name'] = 'BLTU'
                elif self.table[instruction]['func3'] == '111':
                    self.table[instruction]['instr_name'] = 'BGEU'
            elif self.table[instruction]['instr_type'] == 'LW':
                if self.table[instruction]['func3'] == '000':
                    self.table[instruction]['instr_name'] = 'LW'
                elif self.table[instruction]['func3'] == '001':
                    self.table[instruction]['instr_name'] = 'LH'
                elif self.table[instruction]['func3'] == '010':
                    self.table[instruction]['instr_name'] = 'LW'
                elif self.table[instruction]['func3'] == '100':
                    self.table[instruction]['instr_name'] = 'LBU'
                elif self.table[instruction]['func3'] == '101':
                    self.table[instruction]['instr_name'] = 'LHU'
            elif self.table[instruction]['instr_type'] == 'S':
                if self.table[instruction]['func3'] == '000':
                    self.table[instruction]['instr_name'] = 'SB'
                elif self.table[instruction]['func3'] == '001':
                    self.table[instruction]['instr_name'] = 'SH'
                elif self.table[instruction]['func3'] == '010':
                    self.table[instruction]['instr_name'] = 'SW'
                elif self.table[instruction]['func3'] == '011':
                    self.table[instruction]['instr_name'] = 'SW'
                elif self.table[instruction]['func3'] == '100':
                    self.table[instruction]['instr_name'] = 'SD'
            elif self.table[instruction]['instr_type'] == 'U':
                if self.table[instruction]['opcode'] == '0110111':
                    self.table[instruction]['instr_name'] = 'LUI'
                elif self.table[instruction]['opcode'] == '0010111':
                    self.table[instruction]['instr_name'] = 'AUIPC'
            elif self.table[instruction]['instr_type'] == 'J':
                self.table[instruction]['instr_name'] = 'JAL'
            

    def table_lookup(instruction):
        # table lookup for instruction



        return instruction

    def readInstr(self, ReadAddress):
        #read instruction memory
        #return 32 bit hex val
        instruction = ''
        for i in range(len(ReadAddress)):
            if i%4 == 0 and i:
                self.instructions.append(instruction)
                instruction = ''
            
            instruction += ReadAddress[i]
        self.instructions.append(instruction)
        self.fill_opcodes()
        self.fill_destionation_register()
        self.fill_source_register()
        self.fill_function3()
        self.fill_function7()
        self.fill_immediate()
        self.fill_instr_name()
        # print(self.table)
        # for key in self.table.keys():
        #     print(key, self.table[key])
        # print(self.instructions)

    def get_instruction_fromPC(self, PC):
        # get the instruction from the PC
        # return the instruction
        return self.instructions[PC], self.table[self.instructions[PC]]
          
class DataMem(object):
    def __init__(self, name, ioDir):
        self.id = name
        self.ioDir = ioDir
        self.DMem_instructions = []
        with open(ioDir + "./dmem.txt") as dm:
            self.DMem = [data.replace("\n", "") for data in dm.readlines()]
        
        self.readInstr(self.DMem)
        self.dMemFillZeros(len(self.DMem_instructions))
        self.DMem = self.DMem_instructions

    def readInstr(self, ReadAddress):
        #read data memory
        #return 32 bit hex val
        #read instruction memory
        #return 32 bit hex val
        instruction = ''
        for i in range(len(ReadAddress)):
            self.DMem_instructions.append(ReadAddress[i])
        
        # print(self.DMem_instructions)

    def dMemFillZeros(self, curr_len):
        #fill zeros in data memory
        #return 32 bit hex val
        # print(curr_len)
        max_size = MemSize
        if curr_len < max_size * 4:
            for i in range((max_size * 4) - curr_len):
                self.DMem_instructions.append('00000000')
        # print(len(self.DMem_instructions))
        
        
    def writeDataMem(self, Address, WriteData):
        # write data into byte addressable memory
        
        pass
                     
    def outputDataMem(self):
        resPath = self.ioDir + "\\" + self.id + "_DMEMResult.txt"
        with open(resPath, "w") as rp:
            rp.writelines([str(data) + "\n" for data in self.DMem])

class RegisterFile(object):
    def __init__(self, ioDir):
        self.outputFile = ioDir + "RFResult.txt"
        self.Registers = [0x0 for i in range(32)]
    
    def readRF(self, Reg_addr):
        # Fill in
        pass
    
    def writeRF(self, Reg_addr, Wrt_reg_data):
        # Fill in
        pass
         
    def outputRF(self, cycle):
        op = ["-"*70+"\n", "State of RF after executing cycle:" + str(cycle) + "\n"]
        op.extend([str(bin(val)[2:].zfill(32))+"\n" for val in self.Registers])
        if(cycle == 0): perm = "w"
        else: perm = "a"
        with open(self.outputFile, perm) as file:
            file.writelines(op)

class State(object):
    def __init__(self):
        self.IF = {"nop": False, "PC": 0}
        self.ID = {"nop": False, "Instr": 0}
        self.EX = {"nop": False, "Read_data1": 0, "Read_data2": 0, "Imm": 0, "Rs": 0, "Rt": 0, "Wrt_reg_addr": 0, "is_I_type": False, "rd_mem": 0, 
                   "wrt_mem": 0, "alu_op": 0, "wrt_enable": 0}
        self.MEM = {"nop": False, "ALUresult": 0, "Store_data": 0, "Rs": 0, "Rt": 0, "Wrt_reg_addr": 0, "rd_mem": 0, 
                   "wrt_mem": 0, "wrt_enable": 0}
        self.WB = {"nop": False, "Wrt_data": 0, "Rs": 0, "Rt": 0, "Wrt_reg_addr": 0, "wrt_enable": 0}

class Core(object):
    def __init__(self, ioDir, imem, dmem):
        self.myRF = RegisterFile(ioDir)
        self.cycle = 0
        self.halted = False
        self.ioDir = ioDir
        self.state = State()
        self.nextState = State()
        self.ext_imem = imem
        self.ext_dmem = dmem

class SingleStageCore(Core):
    def __init__(self, ioDir, imem, dmem):
        super(SingleStageCore, self).__init__(ioDir + "\\SS_", imem, dmem)
        self.opFilePath = ioDir + "\\StateResult_SS.txt"

        # Modified by me
        # Initialize the PC
        self.PC = 0x0

        # # Initialize the register file
        # self.register_file = RegisterFile(ioDir)

        # print("Single Stage Core Initialized")
        # print("PC: ", self.PC)
        # print("Register File: ", self.co.Registers)

 
    def step(self):
        # My Implementation
        print('---------------------------------------------------------------------------------------')
        old_pc = self.PC
        print("PC: ", self.PC)
        # Fetch the instruction
        instruction, instruction_props = self.ext_imem.get_instruction_fromPC(self.PC//4)
        print(instruction, instruction_props)
    
        if instruction_props['instr_type'] == 'HALT':
            self.halted = True
            self.state.IF['nop'] = True
            print("Register File: ", self.myRF.Registers)
            self.myRF.outputRF(self.cycle)
            self.printState(self.state, self.cycle)
            return
        
        if instruction_props['src_reg1']:
            instruction_props['src_reg1'] = int(instruction_props['src_reg1'], 2)
        if instruction_props['src_reg2']:
            instruction_props['src_reg2'] = int(instruction_props['src_reg2'], 2)
        if instruction_props['dest_reg']:
            instruction_props['dest_reg'] = int(instruction_props['dest_reg'], 2)


        if instruction_props['instr_name'] == 'LW':
            # Load from Memory
            # Get the address from the register file
            address = self.myRF.Registers[instruction_props['src_reg1']]
            address_idx = address
            imm_dec = int(instruction_props['imm'], 2)
            # Get the data from the data memory
            data = ''
            data += self.ext_dmem.DMem[address_idx + imm_dec]
            data += self.ext_dmem.DMem[address_idx+ 1 + imm_dec]
            data += self.ext_dmem.DMem[address_idx+ 2 + imm_dec]
            data += self.ext_dmem.DMem[address_idx+ 3 + imm_dec]
            # data = data[::-1]
            data = int(data, 2)
            print("Data: ", data)
            self.myRF.Registers[instruction_props['dest_reg']] = data
        
        elif instruction_props['instr_name'] == 'SW':
            imm_dec = int(instruction_props['imm'], 2)
            dest_reg_dec = instruction_props['src_reg1']
            src_reg_dec = self.myRF.Registers[instruction_props['src_reg2']]
            print("src_reg_dec: ", src_reg_dec)
            src_bin = str(bin(src_reg_dec)[2:].zfill(32))
            print("dest_reg_dec: ", dest_reg_dec, imm_dec)
            print("src_bin: ", src_bin)
            # write in data memory
            start_idx = dest_reg_dec
            self.ext_dmem.DMem[start_idx + imm_dec] = src_bin[0:8]
            self.ext_dmem.DMem[start_idx + imm_dec + 1] = src_bin[8:16]
            self.ext_dmem.DMem[start_idx + imm_dec + 2] = src_bin[16:24]
            self.ext_dmem.DMem[start_idx + imm_dec + 3] = src_bin[24:32]
        elif instruction_props['instr_name'] == 'ADD':
            result = self.myRF.Registers[instruction_props['src_reg1']] + self.myRF.Registers[instruction_props['src_reg2']]
            binarized_result = str(bin(result)[2:].zfill(32))
            print("bin_result", len(binarized_result))
            if len(binarized_result) > 32:
                binarized_result = binarized_result[-32:]
                result = int(binarized_result, 2)
                print("result: ", result)
            self.myRF.Registers[instruction_props['dest_reg']] = result

        elif instruction_props['instr_name'] == 'SUB':
            result = self.myRF.Registers[instruction_props['src_reg1']] - self.myRF.Registers[instruction_props['src_reg2']]
            binarized_result = str(bin(result)[2:].zfill(32))
            if len(binarized_result) > 32:
                binarized_result = binarized_result[-32:]
                result = int(binarized_result, 2)
            self.myRF.Registers[instruction_props['dest_reg']] = result

        elif instruction_props['instr_name'] == 'XOR':
            result = self.myRF.Registers[instruction_props['src_reg1']] ^ self.myRF.Registers[instruction_props['src_reg2']]
            binarized_result = str(bin(result)[2:].zfill(32))
            if len(binarized_result) > 32:
                binarized_result = binarized_result[-32:]
                result = int(binarized_result, 2)
            self.myRF.Registers[instruction_props['dest_reg']] = result

        elif instruction_props['instr_name'] == 'NOR':
            result = ~(self.myRF.Registers[instruction_props['src_reg1']] | self.myRF.Registers[instruction_props['src_reg2']])
            binarized_result = str(bin(result)[2:].zfill(32))
            if len(binarized_result) > 32:
                binarized_result = binarized_result[-32:]
                result = int(binarized_result, 2)
            self.myRF.Registers[instruction_props['dest_reg']] = result

        elif instruction_props['instr_name'] == 'AND':
            result = self.myRF.Registers[instruction_props['src_reg1']] & self.myRF.Registers[instruction_props['src_reg2']]
            binarized_result = str(bin(result)[2:].zfill(32))
            if len(binarized_result) > 32:
                binarized_result = binarized_result[-32:]
                result = int(binarized_result, 2)
            self.myRF.Registers[instruction_props['dest_reg']] = result

        elif instruction_props['instr_name'] == 'ADDI':
            result = self.myRF.Registers[instruction_props['src_reg1']] + int(instruction_props['imm'], 2)
            binarized_result = str(bin(result)[2:].zfill(32))
            if len(binarized_result) > 32:
                binarized_result = binarized_result[-32:]
                result = int(binarized_result, 2)
            self.myRF.Registers[instruction_props['dest_reg']] = result

        elif instruction_props['instr_name'] == 'ORI':
            result = self.myRF.Registers[instruction_props['src_reg1']] | int(instruction_props['imm'], 2)
            binarized_result = str(bin(result)[2:].zfill(32))
            if len(binarized_result) > 32:
                binarized_result = binarized_result[-32:]
                result = int(binarized_result, 2)
            self.myRF.Registers[instruction_props['dest_reg']] = result
        
        elif instruction_props['instr_name'] == 'XORI':
            result = self.myRF.Registers[instruction_props['src_reg1']] ^ int(instruction_props['imm'], 2)
            binarized_result = str(bin(result)[2:].zfill(32))
            if len(binarized_result) > 32:
                binarized_result = binarized_result[-32:]
                result = int(binarized_result, 2)
            self.myRF.Registers[instruction_props['dest_reg']] = result

        elif instruction_props['instr_name'] == 'ANDI':
            result = self.myRF.Registers[instruction_props['src_reg1']] & int(instruction_props['imm'], 2)
            binarized_result = str(bin(result)[2:].zfill(32))
            if len(binarized_result) > 32:
                binarized_result = binarized_result[-32:]
                result = int(binarized_result, 2)
            self.myRF.Registers[instruction_props['dest_reg']] = result

        elif instruction_props['instr_name'] == 'JAL':
            self.PC = int(instruction_props['imm'], 2)
        
        elif instruction_props['instr_name'] == 'BEQ':
            if self.myRF.Registers[instruction_props['src_reg1']] == self.myRF.Registers[instruction_props['src_reg2']]:
                result = self.PC + int(instruction_props['imm'], 2)
                binarized_result = str(bin(result)[2:].zfill(32))
                if len(binarized_result) > 32:
                    binarized_result = binarized_result[-32:]
                    result = int(binarized_result, 2)
                self.PC = result
                self.PC = self.PC + int(instruction_props['imm'], 2)
            else:
                self.PC += 4
        elif instruction_props['instr_name'] == 'BNE':
            if self.myRF.Registers[instruction_props['src_reg1']] != self.myRF.Registers[instruction_props['src_reg2']]:
                result = self.PC + int(instruction_props['imm'], 2)
                binarized_result = str(bin(result)[2:].zfill(11))
                if len(binarized_result) > 11:
                    binarized_result = binarized_result[-11:]
                    result = int(binarized_result, 2)
                print("result: ", result)
                self.PC = result
            else:
                self.PC += 4

        elif instruction_props['instr_type'] == 'HALT':
            self.halted = True
            return

        self.state.PC = self.PC
        self.state.IF['PC'] = old_pc
        self.state.ID['Instr'] = instruction

        if old_pc == self.PC:
            self.PC += 4    

        self.printState(self.state, self.cycle)




        # Your implementation

        # self.halted = True
        # if self.state.IF["nop"]:
        #     self.halted = True
        print("Register File: ", self.myRF.Registers)
        self.myRF.outputRF(self.cycle) # dump RF
        # self.printState(self.nextState, self.cycle) # print states after executing cycle 0, cycle 1, cycle 2 ... 
            
        self.nextState = State() # initialize for next cycle
        self.nextState.IF['PC'] = self.PC


        self.state = self.nextState #The end of the cycle and updates the current state with the values calculated in this cycle
        self.cycle += 1

        self.step()

    def printState(self, state, cycle):
        printstate = ["-"*70+"\n", "State after executing cycle: " + str(cycle) + "\n"]
        printstate.append("IF.PC: " + str(state.IF["PC"]) + "\n")
        printstate.append("IF.nop: " + str(state.IF["nop"]) + "\n")
        
        if(cycle == 0): perm = "w"
        else: perm = "a"
        with open(self.opFilePath, perm) as wf:
            wf.writelines(printstate)

class FiveStageCore(Core):
    def __init__(self, ioDir, imem, dmem):
        super(FiveStageCore, self).__init__(ioDir + "\\FS_", imem, dmem)
        self.opFilePath = ioDir + "\\StateResult_FS.txt"

        self.fiveStageCurrent = {
            "IF": 0,
            "ID": -1,
            "EX": -1,
            "MEM": -1,
            "WB": -1
        }
        self.fiveStageQueue = []
        self.PC = 0x0


    def step(self):
        print("Five Stage Core Initialized")
        print("PC: ", fsCore.PC)
        # Your implementation
        # self.state.EX['Read_data1'] = self.myRF.Registers[instruction_props['src_reg1']]
        # self.state.EX['Read_data2'] = self.myRF.Registers[instruction_props['src_reg2']]
        # self.state.EX['Imm'] = instruction_props['imm']
        # self.state.EX['Rs'] = instruction_props['src_reg1']
        # self.state.EX['Rt'] = instruction_props['src_reg2']
        # self.state.EX['Wrt_reg_addr'] = instruction_props['dest_reg']
        # self.state.EX['is_I_type'] =  True if instruction_props['instr_type'] == 'I' else False
        # # self.state.EX.rd_mem = instruction_props.rd_mem
        # # self.state.EX.wrt_mem = instruction_props.wrt_mem
        # self.state.EX['alu_op'] = instruction_props['instr_name']
        # self.state.EX['wrt_enable'] = True if instruction_props['dest_reg'] != 0 else False
        # if instruction_props['dest_reg']:
        #     self.state.MEM['ALUresult'] = self.myRF.Registers[instruction_props['dest_reg']]
        # self.state.MEM['Store_data'] = self.myRF.Registers[instruction_props['src_reg2']]
        # self.state.MEM['Rs'] = instruction_props['src_reg1']
        # self.state.MEM['Rt'] = instruction_props['src_reg2']
        # self.state.MEM['Wrt_reg_addr'] = instruction_props['dest_reg']
        # # self.state.MEM.rd_mem = instruction_props.rd_mem
        # # self.state.MEM.wrt_mem = instruction_props.wrt_mem
        # self.state.MEM['wrt_enable'] = True if instruction_props['dest_reg'] != 0 else False
        # if instruction_props['dest_reg']:
        #     self.state.WB['Wrt_data'] = self.myRF.Registers[instruction_props['dest_reg']]
        # self.state.WB['Rs'] = instruction_props['src_reg1']
        # self.state.WB['Rt'] = instruction_props['src_reg2']
        # self.state.WB['Wrt_reg_addr'] = instruction_props['dest_reg']
        # self.state.WB['wrt_enable'] = True if instruction_props['dest_reg'] != 0 else False
        # --------------------- WB stage ---------------------
        
        
        
        # --------------------- MEM stage --------------------
        
        
        
        # --------------------- EX stage ---------------------
        
        
        
        # --------------------- ID stage ---------------------
        
        
        
        # --------------------- IF stage ---------------------


        # My Implementation
        print('---------------------------------------------------------------------------------------')
        while self.fiveStageCurrent['IF'] != self.fiveStageCurrent['WB']:
                # print(self.fiveStageCurrent)
                old_pc = self.PC
                print(self.fiveStageCurrent)
                # print("PC: ", self.PC)
            
                if self.fiveStageCurrent['IF'] >= 0 :
                    nextIF = self.instructionFetch(self.fiveStageCurrent['IF'])

                if self.fiveStageCurrent['ID'] >= 0:
                    self.instructionDecode(self.fiveStageCurrent['ID'])

                if self.fiveStageCurrent['EX'] >= 0:
                    self.execute(self.fiveStageCurrent['EX'])
                
                if self.fiveStageCurrent['MEM'] >= 0:
                    self.memoryAccess(self.fiveStageCurrent['MEM'])

                if self.fiveStageCurrent['WB'] >= 0:
                    self.writeBack(self.fiveStageCurrent['WB'])

                if old_pc == self.PC:
                    self.PC += 4

                self.fiveStageCurrent['WB'] = self.fiveStageCurrent['MEM']
                self.fiveStageCurrent['MEM'] = self.fiveStageCurrent['EX']
                self.fiveStageCurrent['EX'] = self.fiveStageCurrent['ID']
                self.fiveStageCurrent['ID'] = self.fiveStageCurrent['IF']
                if nextIF:
                    self.fiveStageCurrent['IF'] = self.PC

                # print("Register File: ", self.myRF.Registers)
                self.myRF.outputRF(self.cycle) # dump RF
                self.printState(self.state, self.cycle)
                self.cycle += 1
                print('--------------------------------------------------------------------------------------------------------------------------------------------------')
                self.nextState = State()
                self.state = self.nextState 
                
        print(self.fiveStageCurrent)
        if self.fiveStageCurrent['IF'] >= 0 :
            nextIF = self.instructionFetch(self.fiveStageCurrent['IF'])

        if self.fiveStageCurrent['ID'] >= 0:
            self.instructionDecode(self.fiveStageCurrent['ID'])

        if self.fiveStageCurrent['EX'] >= 0:
            self.execute(self.fiveStageCurrent['EX'])
        
        if self.fiveStageCurrent['MEM'] >= 0:
            self.memoryAccess(self.fiveStageCurrent['MEM'])

        if self.fiveStageCurrent['WB'] >= 0:
            self.writeBack(self.fiveStageCurrent['WB'])

        # print("Register File: ", self.myRF.Registers)
        self.myRF.outputRF(self.cycle) # dump RF
        self.printState(self.state, self.cycle)
        self.cycle += 1
        print('--------------------------------------------------------------------------------------------------------------------------------------------------')
        self.nextState = State()
        self.state = self.nextState 

        
        self.halted = True
        if self.state.IF["nop"] and self.state.ID["nop"] and self.state.EX["nop"] and self.state.MEM["nop"] and self.state.WB["nop"]:
            self.halted = True
        
        self.myRF.outputRF(self.cycle) # dump RF
        self.printState(self.nextState, self.cycle) # print states after executing cycle 0, cycle 1, cycle 2 ... 
        
        self.state = self.nextState #The end of the cycle and updates the current state with the values calculated in this cycle
        self.cycle += 1

    def printState(self, state, cycle):
        printstate = ["-"*70+"\n", "State after executing cycle: " + str(cycle) + "\n"]
        printstate.extend(["IF." + key + ": " + str(val) + "\n" for key, val in state.IF.items()])
        printstate.extend(["ID." + key + ": " + str(val) + "\n" for key, val in state.ID.items()])
        printstate.extend(["EX." + key + ": " + str(val) + "\n" for key, val in state.EX.items()])
        printstate.extend(["MEM." + key + ": " + str(val) + "\n" for key, val in state.MEM.items()])
        printstate.extend(["WB." + key + ": " + str(val) + "\n" for key, val in state.WB.items()])

        if(cycle == 0): perm = "w"
        else: perm = "a"
        with open(self.opFilePath, perm) as wf:
            wf.writelines(printstate)

    def writeBack(self, PC):
        instruction, instruction_props = self.ext_imem.get_instruction_fromPC(PC//4)

        if instruction_props['instr_type'] == 'HALT':
            self.state.WB['nop'] = True
            print("HALT: ", "WB")
            return
        else:
            self.state.MEM['nop'] = False
            print("WB: ", instruction_props)

        if instruction_props['src_reg1'] and type(instruction_props['src_reg1']) == str:
            instruction_props['src_reg1'] = int(instruction_props['src_reg1'], 2)
        if instruction_props['src_reg2'] and type(instruction_props['src_reg2']) == str:
            instruction_props['src_reg2'] = int(instruction_props['src_reg2'], 2)
        if instruction_props['dest_reg'] and type(instruction_props['dest_reg']) == str:
            instruction_props['dest_reg'] = int(instruction_props['dest_reg'], 2)

        if instruction_props['dest_reg']:
            self.state.WB['Wrt_data'] = self.myRF.Registers[instruction_props['dest_reg']]
        self.state.WB['Rs'] = instruction_props['src_reg1']
        self.state.WB['Rt'] = instruction_props['src_reg2']
        self.state.WB['Wrt_reg_addr'] = instruction_props['dest_reg']
        self.state.WB['wrt_enable'] = True if instruction_props['dest_reg'] != 0 else False
        # Your implementation
        

    def memoryAccess(self, PC):
        # Your implementation
        instruction, instruction_props = self.ext_imem.get_instruction_fromPC(PC//4)

        if instruction_props['instr_type'] == 'HALT':
            self.state.MEM['nop'] = True
            print("HALT: ", "MEM")
            return
        else:
            self.state.MEM['nop'] = False
            print("MEM: ", instruction_props)

        if instruction_props['src_reg1'] and type(instruction_props['src_reg1']) == str:
            instruction_props['src_reg1'] = int(instruction_props['src_reg1'], 2)

        if instruction_props['src_reg2'] and type(instruction_props['src_reg2']) == str:
            instruction_props['src_reg2'] = int(instruction_props['src_reg2'], 2)

        if instruction_props['dest_reg'] and type(instruction_props['dest_reg']) == str:
            instruction_props['dest_reg'] = int(instruction_props['dest_reg'], 2)


        if instruction_props['dest_reg']:
            self.state.MEM['ALUresult'] = self.myRF.Registers[instruction_props['dest_reg']]
        self.state.MEM['Store_data'] = self.myRF.Registers[instruction_props['src_reg2']] if instruction_props['src_reg2'] else 'None'
        self.state.MEM['Rs'] = instruction_props['src_reg1']
        self.state.MEM['Rt'] = instruction_props['src_reg2']
        self.state.MEM['Wrt_reg_addr'] = instruction_props['dest_reg']
        # self.state.MEM.rd_mem = instruction_props.rd_mem
        # self.state.MEM.wrt_mem = instruction_props.wrt_mem
        self.state.MEM['wrt_enable'] = True if instruction_props['dest_reg'] != 0 else False
        

    def execute(self, PC):
        # Your implementation
        instruction, instruction_props = self.ext_imem.get_instruction_fromPC(PC//4)

        if instruction_props['src_reg1']:
            instruction_props['src_reg1'] = int(instruction_props['src_reg1'], 2)

        if instruction_props['src_reg2']:
            instruction_props['src_reg2'] = int(instruction_props['src_reg2'], 2)

        if instruction_props['dest_reg']:
            instruction_props['dest_reg'] = int(instruction_props['dest_reg'], 2)

        # self.IF = {"nop": False, "PC": 0}
        # self.ID = {"nop": False, "Instr": 0}
        # self.EX = {"nop": False, "Read_data1": 0, "Read_data2": 0, "Imm": 0, "Rs": 0, "Rt": 0, "Wrt_reg_addr": 0, "is_I_type": False, "rd_mem": 0, 
        #            "wrt_mem": 0, "alu_op": 0, "wrt_enable": 0}
        # self.MEM = {"nop": False, "ALUresult": 0, "Store_data": 0, "Rs": 0, "Rt": 0, "Wrt_reg_addr": 0, "rd_mem": 0, 
        #            "wrt_mem": 0, "wrt_enable": 0}
        # self.WB = {"nop": False, "Wrt_data": 0, "Rs": 0, "Rt": 0, "Wrt_reg_addr": 0, "wrt_enable": 0}

        if instruction_props['instr_type'] == 'HALT':
            self.state.EX['nop'] = True
            print("HALT", "execute")
        else:

            self.state.EX['Read_data1'] = str(bin(self.myRF.Registers[instruction_props['src_reg1']])[2:].zfill(32)) if instruction_props['src_reg1']  else 'None'
            self.state.EX['Read_data2'] = str(bin(self.myRF.Registers[instruction_props['src_reg2']])[2:].zfill(32)) if instruction_props['src_reg2'] else 'None'
            self.state.EX['Imm'] = 'None' if 'imm' not in instruction_props.keys() else instruction_props['imm'] 
            self.state.EX['Rs'] = instruction_props['src_reg1']
            self.state.EX['Rt'] = instruction_props['src_reg2']
            self.state.EX['Wrt_reg_addr'] = instruction_props['dest_reg']
            self.state.EX['is_I_type'] =  True if instruction_props['instr_type'] == 'I' else False
            
            self.ALUExecute(instruction, instruction_props)

            print("Execute: ", instruction_props) 
    
        # self.state.EX.rd_mem = instruction_props.rd_mem
        # self.state.EX.wrt_mem = instruction_props.wrt_mem
        self.state.EX['alu_op'] = instruction_props['instr_name']
        self.state.EX['wrt_enable'] = True if instruction_props['dest_reg'] != 0 else False
    

    def instructionDecode(self, PC):
        # Your implementation
        instruction, instruction_props = self.ext_imem.get_instruction_fromPC(PC//4)

        if instruction_props['instr_type'] == 'HALT':
            self.state.ID['nop'] = True

            print("HALT", "Instruction Decode")
        else:
            self.state.ID['nop'] = False
            self.state.ID['instr'] = instruction
            print("Instruction Decode: ", instruction_props)

        

    def instructionFetch(self, PC):

        # First instruction fetch 
        instruction, instruction_props = self.ext_imem.get_instruction_fromPC(PC//4)
        if instruction_props['instr_type'] == 'HALT':
            print("HALT", "Instruction Fetch")
            self.state.IF['PC'] = PC
            self.state.IF['nop'] = True
            return False
        else:
            self.state.IF['PC'] = PC
            self.state.IF['nop'] = False
            print("Instruction Fetch: ", PC)
        return True

    def ALUExecute(self, instruction, instruction_props):
        if instruction_props['instr_name'] == 'LW':
            # Load from Memory
            # Get the address from the register file
            address = self.myRF.Registers[instruction_props['src_reg1']]
            address_idx = address
            imm_dec = int(instruction_props['imm'], 2)
            # Get the data from the data memory
            data = ''
            data += self.ext_dmem.DMem[address_idx + imm_dec]
            data += self.ext_dmem.DMem[address_idx+ 1 + imm_dec]
            data += self.ext_dmem.DMem[address_idx+ 2 + imm_dec]
            data += self.ext_dmem.DMem[address_idx+ 3 + imm_dec]
            # data = data[::-1]
            data = int(data, 2)
            print("Data: ", data)
            self.myRF.Registers[instruction_props['dest_reg']] = data
        
        elif instruction_props['instr_name'] == 'SW':
            imm_dec = int(instruction_props['imm'], 2)
            dest_reg_dec = instruction_props['src_reg1']
            src_reg_dec = self.myRF.Registers[instruction_props['src_reg2']]
            print("src_reg_dec: ", src_reg_dec)
            src_bin = str(bin(src_reg_dec)[2:].zfill(32))
            print("dest_reg_dec: ", dest_reg_dec, imm_dec)
            print("src_bin: ", src_bin)
            # write in data memory
            start_idx = dest_reg_dec
            self.ext_dmem.DMem[start_idx + imm_dec] = src_bin[0:8]
            self.ext_dmem.DMem[start_idx + imm_dec + 1] = src_bin[8:16]
            self.ext_dmem.DMem[start_idx + imm_dec + 2] = src_bin[16:24]
            self.ext_dmem.DMem[start_idx + imm_dec + 3] = src_bin[24:32]
        elif instruction_props['instr_name'] == 'ADD':
            result = self.myRF.Registers[instruction_props['src_reg1']] + self.myRF.Registers[instruction_props['src_reg2']]
            binarized_result = str(bin(result)[2:].zfill(32))
            print("bin_result", len(binarized_result))
            if len(binarized_result) > 32:
                binarized_result = binarized_result[-32:]
                result = int(binarized_result, 2)
                print("result: ", result)
            self.myRF.Registers[instruction_props['dest_reg']] = result

        elif instruction_props['instr_name'] == 'SUB':
            result = self.myRF.Registers[instruction_props['src_reg1']] - self.myRF.Registers[instruction_props['src_reg2']]
            binarized_result = str(bin(result)[2:].zfill(32))
            if len(binarized_result) > 32:
                binarized_result = binarized_result[-32:]
                result = int(binarized_result, 2)
            self.myRF.Registers[instruction_props['dest_reg']] = result

        elif instruction_props['instr_name'] == 'XOR':
            result = self.myRF.Registers[instruction_props['src_reg1']] ^ self.myRF.Registers[instruction_props['src_reg2']]
            binarized_result = str(bin(result)[2:].zfill(32))
            if len(binarized_result) > 32:
                binarized_result = binarized_result[-32:]
                result = int(binarized_result, 2)
            self.myRF.Registers[instruction_props['dest_reg']] = result

        elif instruction_props['instr_name'] == 'NOR':
            result = ~(self.myRF.Registers[instruction_props['src_reg1']] | self.myRF.Registers[instruction_props['src_reg2']])
            binarized_result = str(bin(result)[2:].zfill(32))
            if len(binarized_result) > 32:
                binarized_result = binarized_result[-32:]
                result = int(binarized_result, 2)
            self.myRF.Registers[instruction_props['dest_reg']] = result

        elif instruction_props['instr_name'] == 'AND':
            result = self.myRF.Registers[instruction_props['src_reg1']] & self.myRF.Registers[instruction_props['src_reg2']]
            binarized_result = str(bin(result)[2:].zfill(32))
            if len(binarized_result) > 32:
                binarized_result = binarized_result[-32:]
                result = int(binarized_result, 2)
            self.myRF.Registers[instruction_props['dest_reg']] = result

        elif instruction_props['instr_name'] == 'ADDI':
            result = self.myRF.Registers[instruction_props['src_reg1']] + int(instruction_props['imm'], 2)
            binarized_result = str(bin(result)[2:].zfill(32))
            if len(binarized_result) > 32:
                binarized_result = binarized_result[-32:]
                result = int(binarized_result, 2)
            self.myRF.Registers[instruction_props['dest_reg']] = result

        elif instruction_props['instr_name'] == 'ORI':
            result = self.myRF.Registers[instruction_props['src_reg1']] | int(instruction_props['imm'], 2)
            binarized_result = str(bin(result)[2:].zfill(32))
            if len(binarized_result) > 32:
                binarized_result = binarized_result[-32:]
                result = int(binarized_result, 2)
            self.myRF.Registers[instruction_props['dest_reg']] = result
        
        elif instruction_props['instr_name'] == 'XORI':
            result = self.myRF.Registers[instruction_props['src_reg1']] ^ int(instruction_props['imm'], 2)
            binarized_result = str(bin(result)[2:].zfill(32))
            if len(binarized_result) > 32:
                binarized_result = binarized_result[-32:]
                result = int(binarized_result, 2)
            self.myRF.Registers[instruction_props['dest_reg']] = result

        elif instruction_props['instr_name'] == 'ANDI':
            result = self.myRF.Registers[instruction_props['src_reg1']] & int(instruction_props['imm'], 2)
            binarized_result = str(bin(result)[2:].zfill(32))
            if len(binarized_result) > 32:
                binarized_result = binarized_result[-32:]
                result = int(binarized_result, 2)
            self.myRF.Registers[instruction_props['dest_reg']] = result

        elif instruction_props['instr_name'] == 'JAL':
            self.PC = int(instruction_props['imm'], 2)
        
        elif instruction_props['instr_name'] == 'BEQ':
            if self.myRF.Registers[instruction_props['src_reg1']] == self.myRF.Registers[instruction_props['src_reg2']]:
                result = self.PC + int(instruction_props['imm'], 2)
                binarized_result = str(bin(result)[2:].zfill(32))
                if len(binarized_result) > 32:
                    binarized_result = binarized_result[-32:]
                    result = int(binarized_result, 2)
                self.PC = result
                self.PC = self.PC + int(instruction_props['imm'], 2)
            else:
                self.PC += 4
        elif instruction_props['instr_name'] == 'BNE':
            if self.myRF.Registers[instruction_props['src_reg1']] != self.myRF.Registers[instruction_props['src_reg2']]:
                result = self.PC + int(instruction_props['imm'], 2)
                binarized_result = str(bin(result)[2:].zfill(11))
                if len(binarized_result) > 11:
                    binarized_result = binarized_result[-11:]
                    result = int(binarized_result, 2)
                print("result: ", result)
                self.PC = result
            else:
                self.PC += 4


if __name__ == "__main__":
    
    #parse arguments for input file location
    parser = argparse.ArgumentParser(description='RV32I processor')
    parser.add_argument('--iodir', default="", type=str, help='Directory containing the input files.')
    args = parser.parse_args()

    ioDir = os.path.abspath(args.iodir)
    # print("IO Directory:", ioDir)

    imem = InsMem("Imem", ioDir)
    dmem_ss = DataMem("SS", ioDir)
    dmem_fs = DataMem("FS", ioDir)
    imem_fs = InsMem("Imem", ioDir)
    
    ssCore = SingleStageCore(ioDir, imem, dmem_ss)
    fsCore = FiveStageCore(ioDir, imem_fs, dmem_fs)
    print("Single Stage Core Initialized")
    print("PC: ", ssCore.PC)
    print("Register File: ", ssCore.myRF.Registers)


    while(True):
        if not ssCore.halted:
            ssCore.halted = True
            # ssCore.step()
            # ssCore.cycle += 1
            # ssCore.myRF.outputRF(ssCore.cycle)
            # ssCore.printState(ssCore.state, ssCore.cycle)
        
        if not fsCore.halted:
            fsCore.step()

        if ssCore.halted and fsCore.halted:
            break
    
    # dump SS and FS data mem.
    dmem_ss.outputDataMem()
    dmem_fs.outputDataMem()