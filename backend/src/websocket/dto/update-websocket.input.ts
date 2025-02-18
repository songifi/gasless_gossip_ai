import { CreateWebsocketInput } from './create-websocket.input';
import { PartialType } from '@nestjs/mapped-types';

export class UpdateWebsocketInput extends PartialType(CreateWebsocketInput) {
  id: number;
}
