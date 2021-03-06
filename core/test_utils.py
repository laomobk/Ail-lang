from core.acompiler import (
    ByteCodeFileBuffer,
            LineNumberTableGenerator
        )
from core import aobjects as obj, asts as ast, opcodes as opcs


def unpack_list(l :list):
    rl = []
    for d in l:
        if isinstance(d, tuple):
            rl.append(unpack_list(d))
        else:
            rl.append(make_ast_tree(d))
    return rl

def make_ast_tree(a) -> dict:
    if isinstance(a, ast.CellAST):
        return {'Cell' : {'value' : a.value, 'type' : a.type}}

    elif isinstance(a, ast.PowerExprAST):
        return {'PowerAST' : {'left' : make_ast_tree(a.left), 'right' : make_ast_tree(a.right)}}
    
    elif isinstance(a, ast.ModExprAST):
        return {'ModAST' : {'left' : make_ast_tree(a.left), 'right' : make_ast_tree(a.right)}}

    elif isinstance(a, ast.MuitDivExprAST):
        return {'MDAST' : {'left' : make_ast_tree(a.left), 'right' : make_ast_tree(a.right)}}

    elif isinstance(a, ast.BinaryExprAST):
        return {'BinAST' : {'left' : make_ast_tree(a.left), 'right' : make_ast_tree(a.right)}}

    elif isinstance(a, ast.CallExprAST):
        return {'CallAST' : {'left' : make_ast_tree(a.left), 'arg_list' : make_ast_tree(a.arg_list)}}

    elif isinstance(a, ast.PrintExprAST):
        return {'PrintAST' : {'value' : unpack_list(a.value_list)}}

    elif isinstance(a, ast.InputExprAST):
        return {'InputAST' : {'msg' : make_ast_tree(a.msg), 'list' : make_ast_tree(a.value_list)}}
    
    elif isinstance(a, ast.ArgListAST):
        return {'ArgList' : unpack_list(a.exp_list)}

    elif isinstance(a, ast.ValueListAST):
        return {'ValueList' : unpack_list(a.value_list)}

    elif isinstance(a, ast.DefineExprAST):
        return {'DefAST' : {'name' : a.name, 'value' : make_ast_tree(a.value)}}

    elif isinstance(a, ast.CmpTestAST):
        return {'CmpAST' : {'left' : make_ast_tree(a.left), 'right' : unpack_list(a.right)}}

    elif isinstance(a, ast.AndTestAST):
        return {'AndAST' : {'left' : make_ast_tree(a.left), 'right' : make_ast_tree(a.right)}}

    elif isinstance(a, ast.OrTestAST):
        return {'OrAST' : {'left' : make_ast_tree(a.left), 'right' : make_ast_tree(a.right)}}

    elif isinstance(a, ast.TestExprAST):
        return {'TestAST' : make_ast_tree(a.test)}

    elif isinstance(a, ast.BlockExprAST):
        return {'BlockAST' : unpack_list(a.stmts)}

    elif isinstance(a, ast.IfExprAST):
        return {'IfAST' : 
                {'test' : make_ast_tree(a.test), 
                 'body' : make_ast_tree(a.block), 
                 'else_block' : make_ast_tree(a.else_block)}}

    elif isinstance(a, ast.WhileExprAST):
        return {'WhileAST' : 
                {'test' : make_ast_tree(a.test), 
                 'body' : make_ast_tree(a.block)}}

    elif isinstance(a, ast.DoLoopExprAST):
        return {'DoLoopAST' : 
                {'test' : make_ast_tree(a.test), 
                 'body' : make_ast_tree(a.block)}}

    elif isinstance(a, ast.FunctionDefineAST):
        return {
                'FunctionDefAST' :
                {
                    'name' : a.name,
                    'arg_list' : make_ast_tree(a.arg_list),
                    'block' : make_ast_tree(a.block)}}

    elif isinstance(a, ast.ReturnAST):
        return {'ReturnAST' : {'expr' : make_ast_tree(a.expr)}}

    elif isinstance(a, ast.BreakAST):
        return 'BreakAST'
    
    elif isinstance(a, ast.ContinueAST):
        return 'ContinueAST'

    elif isinstance(a, ast.ArrayAST):
        return {'ArrayAST' : {'items' : make_ast_tree(a.items)}}

    elif isinstance(a, ast.ItemListAST):
        return unpack_list(a.item_list)

    elif isinstance(a, ast.SubscriptExprAST):
        return {'SubscriptExprAST' : 
                {'expr' : make_ast_tree(a.expr),
                 'left' : make_ast_tree(a.left)}}

    elif isinstance(a, ast.LoadAST):
        return {'LoadAST' : {
                 'name' : a.name}}

    elif isinstance(a, ast.MemberAccessAST):
        return {'MemberAccessAST':{
                 'left' : make_ast_tree(a.left),
                 'members' : make_ast_tree(a.members)}}

    elif isinstance(a, ast.AssignExprAST):
        return {'AssignExprAST' : {
                 'left' : make_ast_tree(a.left),
                 'value' : make_ast_tree(a.value)}}

    elif isinstance(a, ast.StructDefineAST):
        return {'StructDefineAST': {
                'name': make_ast_tree(a.name),
                'name_list': make_ast_tree(a.name_list),
                'protected' : make_ast_tree(a.protected_list)}}

    elif isinstance(a, ast.NotTestAST):
        return {'NotTestAST' : {'expr' : make_ast_tree(a.expr)}}

    elif isinstance(a, ast.ForExprAST):
        return {'ForExprAST' : {
                'init' : make_ast_tree(a.init_list),
                'test' : make_ast_tree(a.test),
                'update' : make_ast_tree(a.update_list),
                'block' : make_ast_tree(a.block)}}

    elif isinstance(a, ast.BinaryExprListAST):
        return {'BinExprListAST' : make_ast_tree(a.expr_list)}

    elif isinstance(a, ast.AssignExprListAST):
        return {'AssignListAST' : make_ast_tree(a.expr_list)}

    elif isinstance(a, ast.AssertExprAST):
        return {'AssertExprAST' : make_ast_tree(a.expr)}

    elif isinstance(a, ast.ThrowExprAST):
        return {'ThrowExprAST' : make_ast_tree(a.expr)}

    elif isinstance(a, ast.TryCatchExprAST):
        return {'TryCatchExprAST' :
                    {'try_block' : make_ast_tree(a.try_block),
                     'catch_block' : make_ast_tree(a.catch_block),
                     'finally_block' : make_ast_tree(a.finally_block),
                     'error_name' : make_ast_tree(a.name)}}

    elif isinstance(a, list):
        return unpack_list(a)

    return a


class ByteCodeDisassembler:
    __SHOW_VARNAME = (
                opcs.store_var,
                opcs.load_global,
                opcs.load_local,
                opcs.store_function,
                opcs.load_varname,
                opcs.load_module,
                opcs.load_attr,
                opcs.store_attr,
                opcs.setup_catch
            )

    __SHOW_CONST = (
                opcs.load_const,
            )

    __SHOW_COMPARE_OP = (
                opcs.compare_op,
            )

    __SHOW_JUMPPOINT = (
                opcs.jump_if_false_or_pop,
                opcs.jump_if_true_or_pop,
                opcs.jump_absolute,
                opcs.jump_if_false
            )

    def __init__(self):
        self.__now_buffer :ByteCodeFileBuffer = None

        self.__lnotab_cursor = 0
        self.__offset_counter = 0

        self.__jump_point_table = []

        self.__dis_task = []
    
    @property
    def __lnotab(self) -> LineNumberTableGenerator:
        return self.__now_buffer.lnotab

    @property
    def __varnames(self) -> list:
        return self.__now_buffer.varnames

    @property
    def __consts(self) -> list:
        return self.__now_buffer.consts

    @property
    def __bytecodes(self) -> list:
        return self.__now_buffer.bytecodes.blist \
                if not isinstance(self.__now_buffer, obj.AILCodeObject) \
                else self.__now_buffer.bytecodes

    def __check_lno(self) -> bool:
        if self.__lnotab.table[self.__lnotab_cursor] == self.__offset_counter:
            self.__offset_counter = 0
            self.__move_lnotab_cursor()
            return True
        return False

    def __move_lnotab_cursor(self):
        self.__lnotab_cursor += 2

    def __get_opname(self, opcode :int) -> str:
        for k, v in opcs.__dict__.items():
            if opcode == v:
                return k

    def __get_opcode_comment(self, opcode :int, argv :int) -> str:
        cmt = '( %s )'
        cmts = '( \'%s\' )'

        if opcode in self.__SHOW_CONST:
            c = self.__consts[argv]

            if isinstance(c, obj.AILCodeObject) and c not in self.__dis_task:
                self.__dis_task.append(c)
            
            if type(c) == str:
                return cmts % c
            return cmt % c

        elif opcode in self.__SHOW_VARNAME:
            return cmt % self.__varnames[argv]

        elif opcode in self.__SHOW_COMPARE_OP:
            return cmt % opcs.COMPARE_OPERATORS[argv]

        return ''

    def __check_jump_point(self, opcode :int, argv :int):
        if opcode not in self.__SHOW_JUMPPOINT:
            return

        if argv not in self.__jump_point_table:
            self.__jump_point_table.append(argv)

    def __get_jump_point_commit(self) -> str:
        if self.__offset_counter in self.__jump_point_table:
            self.__jump_point_table.remove(self.__offset_counter)
            return '<<'
        return ''

    def disassemble(self, buffer_ :ByteCodeFileBuffer):
        self.__dis_task.append(buffer_)
        
        while self.__dis_task:
            now_tsk = self.__dis_task.pop(0)

            print('Disassembly of %s:\n' % (now_tsk 
                            if isinstance(now_tsk, obj.AILCodeObject)
                            else now_tsk.code_object))

            self.disassemble_single(now_tsk)

    def disassemble_single(self, buffer_ :ByteCodeFileBuffer):
        self.__now_buffer = buffer_

        #print('lnotab :', self.__now_buffer.lnotab.table)

        self.__move_lnotab_cursor()  # 跳过第一对

        for bi in range(0, len(self.__bytecodes), 2):
            bc = self.__bytecodes[bi]
            argv = self.__bytecodes[bi + 1]

            self.__check_jump_point(bc, argv)

            print('\t', bi, self.__get_opname(bc), argv, 
                    self.__get_opcode_comment(bc, argv), self.__get_jump_point_commit(),
                    sep='\t')

            self.__offset_counter += 2

            #if self.__check_lno():
            #    print()

        print()


def show_bytecode(bf :ByteCodeFileBuffer):
    diser = ByteCodeDisassembler()

    diser.disassemble(bf)


def get_opname(op :int):
    for k, v in opcs.__dict__.items():
        if v == op:
            return k
