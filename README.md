# enum_generator
提取cpp源文件中的enum类型，并生成静态枚举转换表。


举个例子:
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


##        Usage 1:
  python.exe -file single_cpp.cpp [-output enum_table.cpp]
                single_cpp.cpp为待处理的文件cpp文件。本程序会扫描cpp文件中的enum，并生成每个enum的静态表
                enum_table.cpp为生成的文件.如果不指定输出文件，默认生成到：当前路径\enum_table.cpp


##        Usage 2:
  python.exe -files config_file.txt [-output enum_table.cpp]
                config_file.txt文件的内容:每行一个cpp文件。本程序会扫描cpp文件中的enum，并生成每个enum的静态表
                enum_table.cpp为生成的文件.如果不指定输出文件，默认生成到：当前路径\enum_table.cpp
