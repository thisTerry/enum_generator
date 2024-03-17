

struct STUEnumItem
{
	UINT32 m_enumValue;
	const char* m_enumString;
};

enum Color
{
    RED = 0,
    GREEN,
    BLUE
};

static const STUEnumItem s_enumTableOfColor={
	{ Color::RED, "RED" },
	{ Color::GREEN, "GREEN" },
	{ Color::BLUE, "BLUE" },
};

static const UINT32 s_enumTableSizeOfColor = sizeof(s_enumTableOfColor) / sizeof(s_enumTableOfColor[0]);