#!/usr/bin/env python3

__author__ = "Rahul Shekhawat"
__copyright__ = ""
__credits__ = "[Rahul Shekhawat]"
__license__ = "MIT License"
__version__ = "1.0.0"
__email__ = "rahul.shekhawat.dev.mail@gmail.com"
__status__ = "Development"


import xml.etree.ElementTree as ETree

TALENTHITINFO_XML_FILEPATH = r"F:/Game Dev/asset_src/XMLFiles/talent_hit_info.xml"
TALENT_XML_FILEPATH = r"F:/Game Dev/asset_src/XMLFiles/talent.xml"
NPC_XML_FILEPATH = r"F:/Game Dev/asset_src/XMLFiles/npc.xml"

HF_ELUANIMATION_XML_FILEPATH = r"F:\Game Dev\asset_src\Model\Player\hf\hf.elu.animation.xml"
HM_ELUANIMATION_XML_FILEPATH = r"F:\Game Dev\asset_src\Model\Player\hm\hm.elu.animation.xml"

hf_tree = ETree.parse(HF_ELUANIMATION_XML_FILEPATH)
hm_tree = ETree.parse(HM_ELUANIMATION_XML_FILEPATH)
hf_root = hf_tree.getroot()
hm_root = hm_tree.getroot()

hf_AddAnimation_nodes = hf_root.findall("AddAnimation")
hm_AddAnimation_nodes = hm_root.findall("AddAnimation")

talent_xml_tree = ETree.parse(TALENT_XML_FILEPATH)
talent_xml_root = talent_xml_tree.getroot()
TALENT_nodes = talent_xml_root.findall("TALENT")


# Create a map of {talent_hit_id : talent_hit_node}
collision_xml_tree = ETree.parse(TALENTHITINFO_XML_FILEPATH)
collision_xml_root = collision_xml_tree.getroot()
TALENT_HIT_nodes = collision_xml_root.findall("TALENT_HIT")

TALENT_HIT_nodes_dict = {}

for TALENT_HIT_node in TALENT_HIT_nodes:
    HitSegments = TALENT_HIT_node.findall("HitSegment")
    if HitSegments:
        talent_hit_id = TALENT_HIT_node.attrib["id"]
        TALENT_HIT_nodes_dict[talent_hit_id] = TALENT_HIT_node


# Create a map of  {npc_id: npc_node}
npc_xml_tree = ETree.parse(NPC_XML_FILEPATH)
npc_xml_root = npc_xml_tree.getroot()
NPC_nodes = npc_xml_root.findall("NPC")

NPC_nodes_dict = {}
for NPC_node in NPC_nodes:
    npc_id = NPC_node.attrib["id"]
    NPC_nodes_dict[npc_id] = NPC_node


json_obj = {}
for TALENT_node in TALENT_nodes:
    talent_id = TALENT_node.attrib["id"]

    if talent_id not in TALENT_HIT_nodes_dict:
        continue

    if "CastingAni" in TALENT_node.attrib:
        continue

    if "UseAni" not in TALENT_node.attrib:
        continue

    if "WeaponAllowed" in TALENT_node.attrib:
        weapons_string = TALENT_node.attrib["WeaponAllowed"]
        if weapons_string == "ride" or weapons_string == "none":
            continue

        weapons_list = weapons_string.split(",")
        weapons_stripped_list = []
        for weapon in weapons_list:
            weapon_stripped = weapon.strip()
            weapons_stripped_list.append(weapon_stripped)
        
        if len(weapons_stripped_list) == 1:
            animation_name = TALENT_node.attrib["UseAni"]
            animation_name = animation_name.replace("PS_", "")
            animation_name = weapon + "_" + animation_name
            
            animations_set = set()
            animation_filename = None
            for hf_AddAnimation_node in hf_AddAnimation_nodes:
                if animation_name == hf_AddAnimation_node.attrib["name"]:
                    animation_filename = hf_AddAnimation_node.attrib["filename"]
                    animation_filename = animation_filename.replace(".elu.ani", "")

            if animation_filename is not None:
                ue_animation_name = "A_" + animation_filename
                ue_asset_name = ue_animation_name + "." + ue_animation_name
                animation_full_name = "/Game/EOD/Model/Player/hf/hf/ani/" + ue_asset_name
                animations_set.add(animation_full_name)

            animation_filename = None
            for hm_AddAnimation_node in hm_AddAnimation_nodes:
                if animation_name == hm_AddAnimation_node.attrib["name"]:
                    animation_filename = hm_AddAnimation_node.attrib["filename"]
                    animation_filename = animation_filename.replace(".elu.ani", "")
                
            if animation_filename is not None:
                ue_animation_name = "A_" + animation_filename
                ue_asset_name = ue_animation_name + "." + ue_animation_name
                animation_full_name = "/Game/EOD/Model/Player/hm/hm/ani/" + ue_asset_name
                animations_set.add(animation_full_name)
            
            animations_list = list(animations_set)
            if animations_list:
                json_obj[talent_id] = list(animations_set)
                continue

        else:
            TALENT_HIT_nodes_list = []
            for TALENT_HIT_node in TALENT_HIT_nodes:
                talent_hit_id = TALENT_HIT_node.attrib["id"]
                if talent_hit_id == talent_id:
                    TALENT_HIT_nodes_list.append(TALENT_HIT_node)

            if len(TALENT_HIT_nodes_list) == 1:        
                animations_set = set()
                for weapon in weapons_stripped_list:
                    animation_name = TALENT_node.attrib["UseAni"]
                    animation_name = animation_name.replace("PS_", "")
                    animation_name = weapon + "_" + animation_name

                    animation_filename = None
                    for hf_AddAnimation_node in hf_AddAnimation_nodes:
                        if animation_name == hf_AddAnimation_node.attrib["name"]:
                            animation_filename = hf_AddAnimation_node.attrib["filename"]
                            animation_filename = animation_filename.replace(".elu.ani", "")
                    
                    if animation_filename is not None:
                        ue_animation_name = "A_" + animation_filename
                        ue_asset_name = ue_animation_name + "." + ue_animation_name
                        # animation_full_name = "/Game/EOD/Model/Player/hf/hf/ani/A_" + animation_filename
                        animation_full_name = "/Game/EOD/Model/Player/hf/hf/ani/" + ue_asset_name
                        animations_set.add(animation_full_name)
                    
                    animation_filename = None
                    for hm_AddAnimation_node in hm_AddAnimation_nodes:
                        if animation_name == hm_AddAnimation_node.attrib["name"]:
                            animation_filename = hm_AddAnimation_node.attrib["filename"]
                            animation_filename = animation_filename.replace(".elu.ani", "")
                        
                    if animation_filename is not None:
                        ue_animation_name = "A_" + animation_filename
                        ue_asset_name = ue_animation_name + "." + ue_animation_name
                        # animation_full_name = "/Game/EOD/Model/Player/hm/hm/ani/A_" + animation_filename
                        animation_full_name = "/Game/EOD/Model/Player/hm/hm/ani/" + ue_asset_name
                        animations_set.add(animation_full_name)

                animations_list = list(animations_set)
                if animations_list:
                    json_obj[talent_id] = list(animations_set)
                    continue
            else:
                mode_weapons_list = []
                for TALENT_HIT_node in TALENT_HIT_nodes_list:
                    if "Mode" in TALENT_HIT_node.attrib:
                        mode = TALENT_HIT_node.attrib["Mode"]
                        mode_weapons_list.append(mode)

                weapons_stripped_set = set(weapons_stripped_list)
                mode_weapons_set = set(mode_weapons_list)
                no_mode_weapon = list(weapons_stripped_set - mode_weapons_set)[0]

                for TALENT_HIT_node in TALENT_HIT_nodes_list:        
                    animations_set = set()
                    if "Mode" in TALENT_HIT_node.attrib:
                        mode = TALENT_HIT_node.attrib["Mode"]
                        animation_name = TALENT_node.attrib["UseAni"]
                        animation_name = animation_name.replace("PS_", "")
                        animation_name = mode + "_" + animation_name

                        animation_filename = None
                        for hf_AddAnimation_node in hf_AddAnimation_nodes:
                            if animation_name == hf_AddAnimation_node.attrib["name"]:
                                animation_filename = hf_AddAnimation_node.attrib["filename"]
                                animation_filename = animation_filename.replace(".elu.ani", "")
                        
                        if animation_filename is not None:
                            ue_animation_name = "A_" + animation_filename
                            ue_asset_name = ue_animation_name + "." + ue_animation_name
                            animation_full_name = "/Game/EOD/Model/Player/hf/hf/ani/" + ue_asset_name
                            animations_set.add(animation_full_name)
                        
                        animation_filename = None
                        for hm_AddAnimation_node in hm_AddAnimation_nodes:
                            if animation_name == hm_AddAnimation_node.attrib["name"]:
                                animation_filename = hm_AddAnimation_node.attrib["filename"]
                                animation_filename = animation_filename.replace(".elu.ani", "")
                            
                        if animation_filename is not None:
                            ue_animation_name = "A_" + animation_filename
                            ue_asset_name = ue_animation_name + "." + ue_animation_name
                            animation_full_name = "/Game/EOD/Model/Player/hm/hm/ani/" + ue_asset_name
                            animations_set.add(animation_full_name)

                        animations_list = list(animations_set)
                        if animations_list:
                            json_obj[talent_id + '_' + mode] = list(animations_set)
                    else:
                        animation_name = TALENT_node.attrib["UseAni"]
                        animation_name = animation_name.replace("PS_", "")
                        animation_name = no_mode_weapon + "_" + animation_name

                        animation_filename = None
                        for hf_AddAnimation_node in hf_AddAnimation_nodes:
                            if animation_name == hf_AddAnimation_node.attrib["name"]:
                                animation_filename = hf_AddAnimation_node.attrib["filename"]
                                animation_filename = animation_filename.replace(".elu.ani", "")
                        
                        if animation_filename is not None:
                            ue_animation_name = "A_" + animation_filename
                            ue_asset_name = ue_animation_name + "." + ue_animation_name
                            animation_full_name = "/Game/EOD/Model/Player/hf/hf/ani/" + ue_asset_name
                            animations_set.add(animation_full_name)
                        
                        animation_filename = None
                        for hm_AddAnimation_node in hm_AddAnimation_nodes:
                            if animation_name == hm_AddAnimation_node.attrib["name"]:
                                animation_filename = hm_AddAnimation_node.attrib["filename"]
                                animation_filename = animation_filename.replace(".elu.ani", "")
                            
                        if animation_filename is not None:
                            ue_animation_name = "A_" + animation_filename
                            ue_asset_name = ue_animation_name + "." + ue_animation_name
                            animation_full_name = "/Game/EOD/Model/Player/hm/hm/ani/" + ue_asset_name
                            animations_set.add(animation_full_name)
                            
                        animations_list = list(animations_set)
                        if animations_list:
                            json_obj[talent_id] = list(animations_set)


    if "NPC" in TALENT_node.attrib:
        npc_string = TALENT_node.attrib["NPC"]
        npc_list = npc_string.split(",")
        npc_stripped_list = []
        for item in npc_list:
            stripped_item = item.strip()
            npc_stripped_list.append(stripped_item)

        animations_set = set()
        for npc_id in npc_stripped_list:
            if npc_id not in NPC_nodes_dict:
                # print("NPC id:", npc_id, "not found.")
                continue
            NPC_node = NPC_nodes_dict[npc_id]
            if "MeshPath" not in NPC_node.attrib:
                print("Mesh path node not found for npc_id:", npc_id)
                continue

            meshpath_string = NPC_node.attrib["MeshPath"]
            npc_name = meshpath_string.split("/")[1]
            animation_name = TALENT_node.attrib["UseAni"]
            animation_filename = None
            
            eluanimationxml_filepath = "F:/Game dev/asset_src/Model/" + meshpath_string + "/" + npc_name + ".elu.animation.xml"
            try:
                eluanimationxml_tree = ETree.parse(eluanimationxml_filepath)
                eluanimationxml_root = eluanimationxml_tree.getroot()
                AddAnimation_nodes = eluanimationxml_root.findall("AddAnimation")
                for AddAnimation_node in AddAnimation_nodes:
                    if animation_name == AddAnimation_node.attrib["name"]:
                        animation_filename = AddAnimation_node.attrib["filename"]
                        animation_filename = animation_filename.replace(".elu.ani", "")
                        break
            except Exception as e:
                # print(e)
                continue

            if animation_filename is not None:
                ue_animation_name = "A_" + animation_filename
                ue_asset_name = ue_animation_name + "." + ue_animation_name
                animation_full_name = "/Game/EOD/Model/" + meshpath_string + "/" + npc_name + "/ani/" + ue_asset_name
                animations_set.add(animation_full_name)

        animations_list = list(animations_set)
        if animations_list:
            json_obj[talent_id] = list(animations_set)
        
import json
json_stream = open("animation_names.json", "w")
json.dump(json_obj, json_stream)
