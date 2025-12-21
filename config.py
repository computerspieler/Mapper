# Note: The first column's index is 0

# classes.csv configuration
CLIENT_OBF_CLASS_COL=2	# Column of the obfuscated name for the client jar
SERVER_OBF_CLASS_COL=4	# Column of the obfuscated name for the server jar
NON_OBF_CLASS_COL=0		# Column of the correct name
CSV_CLASS_START_ROW=4	# Number of rows to skip at the beginning

# methods.csv configuration
CLIENT_OBF_METHOD_COL=1	# Column of the obfuscated name for the client jar
SERVER_OBF_METHOD_COL=3	# Column of the obfuscated name for the server jar
NON_OBF_METHOD_COL=4	# Column of the correct name
CSV_METHOD_START_ROW=4	# Number of rows to skip at the beginning

# fields.csv configuration
CLIENT_OBF_FIELD_COL=2	# Column of the obfuscated name for the client jar
SERVER_OBF_FIELD_COL=5	# Column of the obfuscated name for the server jar
NON_OBF_FIELD_COL=6		# Column of the correct name
CSV_FIELD_START_ROW=3	# Number of rows to skip at the beginning

# newids.csv configuration
CLIENT_OBF_NEWIDS_COL=0	# Column of the obfuscated name for the client jar
SERVER_OBF_NEWIDS_COL=1	# Column of the obfuscated name for the server jar
NON_OBF_NEWIDS_COL=2	# Column of the correct name
CSV_NEWIDS_START_ROW=0	# Number of rows to skip at the beginning

PACKAGE_DEFAULT="net/minecraft/src/"
PACKAGE_CONSIDERED_DEOBFUSCATED=[
	"paulscode",
	"com/jcraft",
]
