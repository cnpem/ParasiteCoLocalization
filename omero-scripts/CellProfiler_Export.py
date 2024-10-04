import re
from omero import scripts
from omero.gateway import BlitzGateway
from omero.rtypes import rlong, rstring

def parse_name(image_name):
    REGEX = r".* \[(?P<plate_name>.*?) Well (?P<Row>[A-Za-z])(?P<Column>\d+) Field #(?P<Field>\d+)\]"
    return re.match(REGEX, image_name)

class OmeroImageMetadata(object):
    def __init__(self, plate_id, well_id, image_object):
        self.plate_id = plate_id
        self.well_id = well_id
        img = image_object.getImage()
        self.image_id = img.getId()
        self.image_name = img.getName()
        self.size_x = img.getSizeX()
        self.size_y = img.getSizeY()
        self.size_z = img.getSizeZ()
        self.size_c = img.getSizeC()
        self.size_t = img.getSizeT()
        self.pixel_size_x = img.getPixelSizeX()
        self.pixel_size_y = img.getPixelSizeY()
        self.pixel_size_z = img.getPixelSizeZ()
        # self.z = img.getZ()
        # self.t = img.getT()
        match = parse_name(self.image_name)
        if match:
            self.plate_name = match.group("plate_name")
            self.row = match.group("Row")
            self.column = match.group("Column")
            self.field = match.group("Field")
        else:
            self.plate_name = None
            self.row = None
            self.column = None
            self.field = None
        self.channel_labels = img.getChannelLabels()

    def __str__(self):
        def row(channel):
            return (
                f"omero:iid={self.image_id}, {self.image_id}, {self.image_name}, {self.plate_id}, {self.plate_name}, "
                f"{self.well_id}, {self.row}, {self.column}, {self.field}, "
                f"{self.size_x}, {self.size_y}, {self.size_z}, {self.size_c}, {self.size_t}, "
                f"{self.pixel_size_x}, {self.pixel_size_y}, {self.pixel_size_z}, "
                # f"{self.z}, {self.t}, "
                f"{channel[0]}, {channel[1]}\n"
            )

        return "".join([row(channel) for channel in enumerate(self.channel_labels)])

    @staticmethod
    def get_csv_header():
        return (
            "File,ImageID,ImageName,PlateID,PlateName,"
            "WellID,Row,Column,Field,"
            "SizeX,SizeY,SizeZ,SizeC,SizeT,"
            "PixelSizeX,PixelSizeY,PixelSizeZ,"
            # "Z,T,"
            "C,ChannelName\n"
        )
   
def link_annotation(objects, file_ann):
    """Link the File Annotation to each object."""
    for o in objects:
        if o.canAnnotate():
            o.linkAnnotation(file_ann)

def plate_csv_export(conn: BlitzGateway, script_params):
    dtype = script_params['Data_Type']
    ids = script_params['Plate_ID']
    csv_header = OmeroImageMetadata.get_csv_header()

    if dtype == "Plate":
        for plate in conn.getObjects("Plate", ids):
            if plate == None: 
                print(f"Plate {plate_id} not found")
                break
            
            plate_id = plate.getId()
            file_name = f"omero-plate-{plate_id}.csv"

            with open(file_name, "w") as csv_file:
                csv_file.write(csv_header)
                for well in plate.listChildren():
                    well_id = well.getId()
                    for image in well.listChildren():
                        img_metadata = OmeroImageMetadata(plate_id, well_id, image)
                        csv_file.write(str(img_metadata))
            
            file_ann = conn.createFileAnnfromLocalFile(file_name, mimetype="text/csv")

            objects = conn.getObjects(dtype, ids)
            link_annotation(objects, file_ann)
        

def run_script():
    data_types = [rstring(s) for s in ['Screen', 'Plate', 'Project', 'Dataset', 'Image']]

    client = scripts.client(
        "CellProfiler_Export.py", """This script ...""",

        scripts.String(
            "Data_Type", optional=False, grouping="1",
            description="Choose source of images (only Plate supported)",
            values=data_types, default="Plate"),

        scripts.List(
            "Plate_ID", optional=False, grouping="2",
            description="List of Plates IDs to process.").ofType(rlong(0)),

        version="0.1",
        authors=["ILUM"],
        institutions=["LNBio","ILUM","CNPEM"],
        contact="edb@lnbio.cnpem.br",
    )

    try:
        conn = BlitzGateway(client_obj=client)
        script_params = client.getInputs(unwrap=True)
        print("**** Params ****")
        print(script_params)
        plate_csv_export(conn,script_params)
        client.setOutput("Message", rstring("Success"))

    finally:
        client.closeSession()


if __name__ == "__main__":
  run_script()
