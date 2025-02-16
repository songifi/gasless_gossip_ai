import { CreateChatInput } from './create-chat.input';
import { PartialType } from '@nestjs/mapped-types';

export class UpdateChatInput extends PartialType(CreateChatInput) {
  id: number;
}
