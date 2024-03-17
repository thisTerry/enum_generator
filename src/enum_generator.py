# enum_generator.py

import clang.cindex as CX
import sys

def print_usage():
	print("""\033[0;36;40m
	开发者：dingyk 邮箱：iamkun2005@163.com
	作用：提取cpp源文件中的enum类型，并生成一张静态枚举转换表。
	\033[0m""")
	
	print("""\033[0;32;40m举个例子:
	cpp文件的定义如下：	
	enum Color
	{
		RED = 0,
		GREEN,
		BLUE
	};
	
	约定静态表项的定义如下：	
	struct STUEnumItem
	{
		int m_enumValue;
		const char* m_enumString;
	};


	生成的静态表如下：
	static const STUEnumItem s_enumTableOfColor={
		{ Color::RED, "RED" },
		{ Color::GREEN, "GREEN" },
		{ Color::BLUE, "BLUE" },
	};
	static const UINT32 s_enumTableSizeOfColor = sizeof(s_enumTableOfColor) / sizeof(s_enumTableOfColor[0]);
	\033[0m""")
	
	print("""\033[0;35;40m
	Usage 1:\n  python.exe -file single_cpp.cpp [-output enum_table.cpp]
	\tsingle_cpp.cpp为待处理的文件cpp文件。本程序会扫描cpp文件中的enum，并生成每个enum的静态表
	\tenum_table.cpp为生成的文件.如果不指定输出文件，默认生成到：当前路径\\enum_table.cpp
	\033[0m""")
	
	print("""\033[0;35;40m
	Usage 2:\n  python.exe -files config_file.txt [-output enum_table.cpp]
	\tconfig_file.txt文件的内容:每行一个cpp文件。本程序会扫描cpp文件中的enum，并生成每个enum的静态表
	\tenum_table.cpp为生成的文件.如果不指定输出文件，默认生成到：当前路径\\enum_table.cpp
	\033[0m""")

def add_cpp_files(file, list):
	try:
		with open(file, "r", encoding="utf-8") as f:
			lines = f.readlines()
			for line in lines:
				list.append(line)
	except Exception as e:
		print(e)

def traverse_enum(node: CX.Cursor):
	if node.kind == CX.CursorKind.ENUM_DECL:
		print(f"static const STUEnumItem s_enumTableOf{node.spelling}[]={{")
		for child in node.get_children():
			print(f'\t{{ {node.spelling}::{child.spelling}, \"{child.spelling}\" }},')
		print(f"}};")
		print(f"static const UINT32 s_enumTableSizeOf{node.spelling} = sizeof(s_enumTableOf{node.spelling}) / sizeof(s_enumTableOf{node.spelling}[0]);\n")
		
	for child in node.get_children():
		traverse_enum(child)
		
def traverse_enum_tofile(node: CX.Cursor, f):
	if node.kind == CX.CursorKind.ENUM_DECL:
		f.write(f"static const STUEnumItem s_enumTableOf{node.spelling}[]={{\n")
		for child in node.get_children():
			f.write(f'\t{{ {node.spelling}::{child.spelling}, \"{child.spelling}\" }},\n')
		f.write(f"}};\n")
		f.write(f"static const UINT32 s_enumTableSizeOf{node.spelling} = sizeof(s_enumTableOf{node.spelling}) / sizeof(s_enumTableOf{node.spelling}[0]);\n\n")
		
	for child in node.get_children():
		traverse_enum_tofile(child,f)
		
if __name__ == "__main__":
	sys_argc = len(sys.argv)#入参数量
	cpp_files = []#文件列表
	output_file = "enum_table.cpp"
	
	error = False
	if sys_argc < 3:
		print_usage()
		error = True
		
	if sys_argc >= 3:
		config_file=""
		if "-files" == sys.argv[1]:
			add_cpp_files(sys.argv[2],cpp_files)
		elif "-file" == sys.argv[1]:
			cpp_files.append(sys.argv[2])
		else:
			print_usage()
			error = True
			
	if sys_argc >= 5:
		if "-output" == sys.argv[3]:
			output_file= sys.argv[4]
			print(output_file)
		else:
			print_usage()
			error = True

	if not error:
		index = CX.Index.create(excludeDecls=True)
		try:
			with open (output_file, "w", encoding="utf-8") as f:
				for cpp_file in cpp_files:
					tu = index.parse(cpp_file, args=['-std=c++20'])
					traverse_enum_tofile(tu.cursor, f)
		except Exception as e:
			print(e)
		