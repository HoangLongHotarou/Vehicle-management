import 'package:flutter/material.dart';
import 'package:license_plate_detect/core/theme/app_color.dart';

import '../../../core/models/vehicle_info.dart';
import '../../../core/theme/app_data.dart';

class VehicleItem extends StatelessWidget {
  const VehicleItem({
    Key? key,
    required this.vehicles,
    required this.index,
  }) : super(key: key);

  final List<VehicleInfo> vehicles;
  final int index;

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: EdgeInsets.only(bottom: 12),
      padding: EdgeInsets.all(8),
      decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(12),
              border: Border.all(color: AppColor.primaryColor,width: 1)),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.start,
        children: [
          Container(
            padding: EdgeInsets.all(8),
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(8),
              color: Colors.grey[200],
              border: Border.all(color: AppColor.primaryColor,width: 1)),
            child: vehicles[index].type == 'motorcycle' 
              ? Image.asset(AppData.icMotobike,width: 32,) 
              : Image.asset(AppData.icCar,width: 32,),
          ) ,
          const SizedBox(width: 24,),
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(vehicles[index].plate!,style: Theme.of(context).textTheme.titleLarge!.copyWith(color: AppColor.primaryColor,fontSize: 20),),
              Text(vehicles[index].type!,style: Theme.of(context).textTheme.titleSmall!.copyWith(color: Colors.grey),),
            ],
          )
        ]
      ),
    );
  }
}